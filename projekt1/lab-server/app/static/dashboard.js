'use strict';

const $ = (id) => document.getElementById(id);
const MAX_LOG = 1000;

const ui = {
  config: null,
  snap: null,
  clockOffset: 0,          // server_time - czas przeglądarki
  messages: [],            // najstarsze pierwsze
  openBodies: new Set(),   // id komunikatów z rozwiniętą treścią
  bodies: new Map(),
  selected: new Set(),
  detail: null,            // indeks klienta w oknie szczegółów
  charts: {},
};

const STATUS = {
  registered: ['', 'zarejestrowany'],
  preparing: ['sending', 'generowanie danych'],
  sending: ['sending', 'wysyłanie'],
  processing: ['processing', 'przetwarza'],
  waiting_reference: ['processing', 'czeka na wzorzec'],
  error: ['critical', 'błąd'],
};
const KIND = { handshake: 'handshake', start: 'start', data: 'dane', result: 'wynik', invalid: 'niepoprawne' };

function esc(v) {
  return String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const fmtSec = (s) => (s == null ? '–' : s.toFixed(3));
const fmtInt = (n) => (n == null ? '–' : n.toLocaleString('pl-PL'));
const fmtTime = (ts) => new Date(ts * 1000).toLocaleTimeString('pl-PL', { hour12: false }) +
  '.' + String(Math.floor((ts % 1) * 1000)).padStart(3, '0');
const fmtSize = (b) => (b < 1024 ? `${b} B` : b < 1048576 ? `${(b / 1024).toFixed(1)} kB` : `${(b / 1048576).toFixed(1)} MB`);
const serverNow = () => Date.now() / 1000 + ui.clockOffset;

async function api(path, opts = {}) {
  const res = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...opts });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || res.statusText);
  return data;
}

// ---------------------------------------------------------------- start
async function init() {
  ui.config = await api('/api/config');
  $('days').value = ui.config.days;
  $('cars').value = ui.config.cars_per_10_spots;
  $('parkings').innerHTML = ui.config.parkings.map((p, i) =>
    `<span class="chip"><span class="swatch" style="background:var(--s${i + 1})"></span>
     <b>${p}</b> ${ui.config.capacity[p]} miejsc · ${ui.config.rate[p].toFixed(2)} zł/min</span>`).join('') +
    `<span class="chip">endpoint klienta: <code>POST ${esc(ui.config.client_path)}</code></span>`;
  renderVariants();
  renderNetwork();
  bindEvents();
  connect();
  setInterval(tick, 100);
}

function connect() {
  const last = ui.messages.length ? ui.messages[ui.messages.length - 1].id : 0;
  const es = new EventSource(`/api/stream?last_id=${last}`);
  es.onopen = () => setConn('live', 'na żywo');
  es.onerror = () => setConn('down', 'brak połączenia – ponawiam…');
  es.addEventListener('state', (e) => onState(JSON.parse(e.data)));
  es.addEventListener('messages', (e) => onMessages(JSON.parse(e.data)));
}

function setConn(cls, text) {
  $('conn').className = `conn ${cls}`;
  $('connText').textContent = text;
}

function onState(snap) {
  ui.snap = snap;
  ui.clockOffset = snap.server_time - Date.now() / 1000;
  for (const upd of snap.message_updates) {
    const m = ui.messages.find((x) => x.id === upd.id);
    if (m && m.status !== upd.status) { Object.assign(m, upd); patchLogRow(m); }
  }
  const known = new Set(snap.clients.map((c) => c.indeks));
  for (const i of ui.selected) if (!known.has(i)) ui.selected.delete(i);
  renderKpis();
  renderClients();
  renderRanking();
  renderLeader();
  renderRuns();
  renderStartState();
  if (ui.detail != null && $('detail').open) {
    const c = snap.clients.find((x) => x.indeks === ui.detail);
    const run = c && snap.runs.find((r) => r.id === c.run);
    const sig = c ? `${c.status}|${c.run}|${c.score}|${c.history.length}|${run ? run.reference_status : ''}` : '';
    if (sig !== ui.detailSig) { ui.detailSig = sig; refreshDetail(); }
  }
}

function onMessages(msgs) {
  if (!ui.messages.length && msgs.length) {
    ui.messages.push(...msgs);
    renderLog();
    return;
  }
  ui.messages.push(...msgs);
  if (ui.messages.length > MAX_LOG) ui.messages.splice(0, ui.messages.length - MAX_LOG);
  const body = $('logBody');
  const newest = $('fFollow').checked;
  for (const m of msgs) {
    if (!matches(m)) continue;
    const tr = logRow(m);
    tr.classList.add('fresh');
    if (newest) body.prepend(tr); else body.append(tr);
  }
  while (body.querySelectorAll('tr.row').length > MAX_LOG) {
    const rows = body.querySelectorAll('tr.row');
    removeLogRow(newest ? rows[rows.length - 1] : rows[0]);
  }
  $('logEmpty').hidden = body.children.length > 0;
}

// ---------------------------------------------------------------- KPI
function renderKpis() {
  const s = ui.snap;
  const clients = s.clients;
  const done = clients.filter((c) => c.status === 'done');
  const perfect = done.filter((c) => c.score === c.total).length;
  const active = clients.filter((c) => c.status === 'sending' || c.status === 'processing').length;
  const lastRun = s.runs[s.runs.length - 1];
  const lastGood = lastRun ? clients.flatMap((c) => c.history.filter((h) => h.run === lastRun.id && h.score === h.total)
    .map((h) => ({ indeks: c.indeks, duration: h.duration }))) : [];
  const bestEntry = lastGood.sort((x, y) => x.duration - y.duration)[0];
  const tiles = [
    ['Klienci', fmtInt(clients.length), active ? `${active} w trakcie` : 'zarejestrowani'],
    ['Uruchomienia', fmtInt(s.runs.length), s.busy ? 'wysyłanie…' : (s.runs.length ? `ostatnie #${s.runs[s.runs.length - 1].id}` : 'brak')],
    ['Wyniki poprawne', `${perfect}/${done.length}`, 'ostatnie wyniki klientów'],
    ['Najlepszy czas', bestEntry ? `${bestEntry.duration.toFixed(3)} s` : '–',
      lastRun ? `#${lastRun.id} ${lastRun.variant || 'ręczny'}${bestEntry ? ` · indeks ${bestEntry.indeks}` : ''}` : ''],
    ['Wysłane zdarzenia', fmtInt(s.totals.events_sent), 'łącznie'],
    ['Komunikaty', fmtInt(s.totals.messages), `${fmtInt(s.totals.errors)} błędów`],
  ];
  $('kpis').innerHTML = tiles.map(([l, v, sub]) =>
    `<div class="kpi"><div class="label">${l}</div><div class="value">${esc(v)}</div><div class="sub">${esc(sub)}</div></div>`).join('');
}

// ---------------------------------------------------------------- klienci
function statusBadge(c) {
  if (c.status === 'done') {
    return c.score === c.total
      ? '<span class="badge good"><i></i>✓ poprawny</span>'
      : '<span class="badge serious"><i></i>⚠ błędy w wyniku</span>';
  }
  const [cls, label] = STATUS[c.status] || ['', c.status];
  return `<span class="badge ${cls}"${c.error ? ` title="${esc(c.error)}"` : ''}><i></i>${c.status === 'error' ? '✕ ' : ''}${label}</span>`;
}

function addrWarning(c) {
  const local = ['localhost', '127.0.0.1'];
  if (c.source_ip && local.includes(c.ip_addr) && !['127.0.0.1', '::1'].includes(c.source_ip)) {
    return `<div class="warn" title="Klient zgłosił się z ${esc(c.source_ip)}, ale jako swój adres podał ${esc(c.ip_addr)} – serwer nie wyśle mu danych. Popraw CLIENT_IP.">⚠ zgłoszenie z ${esc(c.source_ip)}</div>`;
  }
  return '';
}

function scoreCell(c) {
  if (c.score == null) return '<span class="muted">–</span>';
  const pct = c.total ? (100 * c.score) / c.total : 0;
  return `<div class="score"><div class="bar"><span class="${c.score === c.total ? '' : 'partial'}" style="width:${pct}%"></span></div>
          <span class="txt">${c.score}/${c.total}</span></div>` +
    (c.n_differences ? `<div class="muted">${c.n_differences} różnic</div>` : '');
}

function renderClients() {
  const clients = ui.snap.clients;
  $('clientsEmpty').hidden = clients.length > 0;
  $('clientsInfo').textContent = clients.length ? `${clients.length} zarejestrowanych · zaznaczonych: ${ui.selected.size}` : '';
  $('clientsBody').innerHTML = clients.map((c) => {
    const best = c.history.filter((h) => h.score === h.total).map((h) => h.duration);
    return `<tr data-indeks="${c.indeks}">
      <td><input type="checkbox" class="sel" ${ui.selected.has(c.indeks) ? 'checked' : ''} aria-label="Zaznacz ${c.indeks}"></td>
      <td><b>${c.indeks}</b></td>
      <td class="mono">${esc(c.ip_addr)}:${c.port}${addrWarning(c)}</td>
      <td>${statusBadge(c)}${c.error ? `<div class="muted">${esc(c.error)}</div>` : ''}</td>
      <td class="num">${c.run == null ? '–' : '#' + c.run}</td>
      <td class="num">${fmtInt(c.events || null)}</td>
      <td class="num elapsed" data-sent="${c.sent_at ?? ''}" data-status="${c.status}">${fmtSec(c.duration)}</td>
      <td class="num" title="${c.transfer == null ? '' : `transfer i odbiór danych: ${c.transfer.toFixed(3)} s`}">${c.result_before_ack && c.status === 'done'
        ? '<span class="warn" title="wynik dotarł przed potwierdzeniem odbioru danych – klient liczył przed odpowiedzią 201">⚠</span>'
        : fmtSec(c.processing)}</td>
      <td class="num">${c.speedup == null ? '–' : '×' + c.speedup.toFixed(2)}</td>
      <td>${scoreCell(c)}</td>
      <td class="num">${best.length ? Math.min(...best).toFixed(3) : '–'}</td>
      <td class="actions">
        <button class="small" data-act="detail">Szczegóły</button>
        <button class="small ghost" data-act="remove" title="Usuń klienta">✕</button>
      </td></tr>`;
  }).join('');
  $('selectAll').checked = clients.length > 0 && ui.selected.size === clients.length;
  tick();
}

// licznik czasu na żywo dla klientów, którzy jeszcze liczą
function tick() {
  for (const td of document.querySelectorAll('td.elapsed')) {
    const st = td.dataset.status;
    if ((st === 'processing' || st === 'sending') && td.dataset.sent) {
      td.textContent = (serverNow() - parseFloat(td.dataset.sent)).toFixed(1) + '…';
    }
  }
}

function renderStartState() {
  const s = ui.snap;
  const target = $('target').value;
  const count = target === 'all' ? s.clients.length : ui.selected.size;
  $('startBtn').disabled = s.busy || count === 0;
  for (const b of document.querySelectorAll('.variant')) b.disabled = s.busy || count === 0;
  $('startInfo').textContent = s.busy ? 'trwa wysyłanie danych…'
    : count === 0 ? (target === 'all' ? 'brak klientów' : 'nie zaznaczono klientów')
      : `dane zostaną wysłane do ${count} ${count === 1 ? 'klienta' : 'klientów'} – wybierz wariant`;
}

function targetClients() {
  return $('target').value === 'all' ? null : [...ui.selected];
}

async function startRun(clients, variant = null) {
  const body = variant ? { variant, clients } : {
    days: parseInt($('days').value, 10),
    cars_per_10_spots: parseInt($('cars').value, 10),
    clients,
  };
  try {
    await api('/api/start', { method: 'POST', body: JSON.stringify(body) });
  } catch (e) {
    $('startInfo').textContent = `Nie udało się: ${e.message}`;
  }
}

// ---------------------------------------------------------------- adres serwera
async function renderNetwork() {
  let net;
  try { net = await api('/api/network'); } catch { return; }
  const ip = net.addresses[0] || location.hostname;
  $('connectSnippet').textContent = `SERVER_IP = '${ip}'\nSERVER_PORT = ${net.port}`;
  const extra = [];
  if (net.addresses.length > 1) extra.push(`inne adresy tej maszyny: ${net.addresses.slice(1).map(esc).join(', ')}`);
  extra.push(`nazwa hosta: ${esc(net.hostname)} · CLIENT_IP = adres komputera studenta w tej samej sieci`);
  if (net.local_only) {
    extra.push(`<span class="warn">⚠ serwer nasłuchuje tylko na ${esc(net.bound_host)} – inne komputery się nie połączą.
      Uruchom: <code>python -m uvicorn main:app --host 0.0.0.0 --port ${net.port}</code></span>`);
  }
  $('connectExtra').innerHTML = extra.map((x) => `<span>${x}</span>`).join('');
}

// ---------------------------------------------------------------- warianty
function renderVariants() {
  const vs = ui.config.variants;
  const levels = [...new Map(vs.map((v) => [v.rejections, v.rejection_rate])).entries()];
  const sizes = [...new Map(vs.map((v) => [v.size, v.expected_time])).entries()];
  let html = '<div class="corner"></div>' +
    levels.map(([name, rate]) => `<div class="hdr">${esc(name)} (${esc(rate)})</div>`).join('');
  for (const [size, time] of sizes) {
    html += `<div class="rowhdr">${esc(size)}<span>${esc(time)} jednowątkowo</span></div>`;
    for (const v of vs.filter((x) => x.size === size)) {
      const events = v.days * v.cars_per_10_spots * 12.3;
      html += `<button class="variant" data-variant="${esc(v.id)}" title="${v.days} dni, obciążenie ${v.cars_per_10_spots}">
        <b>${esc(v.id)}</b><span>~${fmtInt(Math.round(events / 1000))} tys. zdarzeń · ${v.days} dni</span></button>`;
    }
  }
  $('variants').innerHTML = html;
}

const variantName = (id) => {
  const v = ui.config.variants.find((x) => x.id === id);
  return v ? `${v.id} · ${v.size}, ${v.rejections}` : 'własne parametry';
};

// ---------------------------------------------------------------- ranking studentów
function leaderboard() {
  const ids = ui.config.variants.map((v) => v.id);
  const best = {};  // wariant -> najlepszy poprawny czas wśród wszystkich
  const rows = ui.snap.clients.map((c) => {
    const cells = {};
    for (const h of c.history) {
      if (!h.variant || !ids.includes(h.variant)) continue;
      const cell = cells[h.variant] ||= { best: null, attempts: 0 };
      cell.attempts += 1;
      if (h.score === h.total && (cell.best == null || h.duration < cell.best)) { cell.best = h.duration; cell.speedup = h.speedup; }
    }
    for (const [v, cell] of Object.entries(cells)) {
      if (cell.best != null && (best[v] == null || cell.best < best[v])) best[v] = cell.best;
    }
    return { c, cells };
  }).filter((r) => Object.keys(r.cells).length);
  for (const r of rows) {
    const solved = Object.entries(r.cells).filter(([, x]) => x.best != null);
    r.solved = solved.length;
    r.loss = solved.length ? solved.reduce((a, [v, x]) => a + x.best / best[v], 0) / solved.length : Infinity;
    r.attempts = Object.values(r.cells).reduce((a, x) => a + x.attempts, 0);
  }
  rows.sort((a, b) => b.solved - a.solved || a.loss - b.loss || a.c.indeks - b.c.indeks);
  return { ids, best, rows };
}

function renderLeader() {
  const { ids, best, rows } = leaderboard();
  $('leaderEmpty').hidden = rows.length > 0;
  $('leader').hidden = rows.length === 0;
  if (!rows.length) return;
  let html = '<thead><tr><th class="place">#</th><th>Indeks</th>' + ids.map((v) => `<th title="${esc(variantName(v))}">${v}</th>`).join('') +
    '<th>Rozwiązane</th><th title="średnio: najlepszy czas klienta / najlepszy czas w wariancie">Strata</th><th>Próby</th></tr></thead><tbody>';
  rows.forEach((r, i) => {
    html += `<tr><td class="place">${i + 1}</td><td><b>${r.c.indeks}</b></td>`;
    for (const v of ids) {
      const cell = r.cells[v];
      if (!cell) html += '<td class="muted">–</td>';
      else if (cell.best == null) html += `<td class="fail" title="${cell.attempts} prób, żadna poprawna">✕</td>`;
      else html += `<td class="${cell.best === best[v] ? 'best' : ''}" title="${cell.attempts} prób${cell.speedup ? ` · przyspieszenie ×${cell.speedup.toFixed(2)}` : ''}${cell.best === best[v] ? ' · najszybszy w wariancie' : ''}">${cell.best.toFixed(3)}</td>`;
    }
    html += `<td>${r.solved}/${ids.length}</td><td>${r.solved ? '×' + r.loss.toFixed(3) : '–'}</td><td>${r.attempts}</td></tr>`;
  });
  $('leader').innerHTML = html + '</tbody>';
}

// ---------------------------------------------------------------- eksperymenty
function refCell(r) {
  if (r.reference_status === 'done') return `<span title="całość z parsowaniem JSON: ${r.reference_time.toFixed(3)} s">${r.reference_processing.toFixed(3)}</span>`;
  if (r.reference_status === 'error') return `<span class="status-bad" title="${esc(r.reference_error)}">✕ błąd</span>`;
  return r.reference_status === 'running' ? '<span class="status-wait">liczy…</span>' : '–';
}

function renderRuns() {
  const runs = [...ui.snap.runs].reverse();
  $('runsEmpty').hidden = runs.length > 0;
  $('runsBody').innerHTML = runs.map((r) => {
    const results = ui.snap.clients.flatMap((c) => c.history.filter((h) => h.run === r.id));
    const good = results.filter((h) => h.score === h.total);
    const bestTime = good.length ? Math.min(...good.map((h) => h.duration)).toFixed(3) : '–';
    return `<tr data-run="${r.id}">
      <td class="num">${r.id}</td>
      <td class="mono">${fmtTime(r.started_at).slice(0, 8)}</td>
      <td>${esc(variantName(r.variant))}</td>
      <td class="num">${fmtInt(r.days)}</td>
      <td class="num">${r.cars_per_10_spots}</td>
      <td>${r.clients.length === 1 ? r.clients[0] : `${r.clients.length} klientów`}</td>
      <td class="num">${refCell(r)}</td>
      <td>${results.length}/${r.clients.length} odebranych · ${good.length} poprawnych</td>
      <td class="num">${bestTime}</td>
      <td class="actions"><button class="small ghost" data-act="del-run">Usuń</button></td></tr>`;
  }).join('');
}

// ---------------------------------------------------------------- ranking
function chartDefaults() {
  Chart.defaults.font.family = 'system-ui, -apple-system, "Segoe UI", sans-serif';
  Chart.defaults.font.size = 12;
  Chart.defaults.color = css('--muted');
  Chart.defaults.borderColor = css('--grid');
}

function tooltipStyle() {
  return {
    backgroundColor: css('--text'), titleColor: css('--surface'), bodyColor: css('--surface'),
    padding: 8, cornerRadius: 6, displayColors: true, boxPadding: 4,
  };
}

function renderRanking() {
  const s = ui.snap;
  const rows = s.clients.filter((c) => c.status === 'done').sort((a, b) => a.duration - b.duration);
  $('rankingEmpty').hidden = rows.length > 0;
  $('rankingBox').hidden = rows.length === 0;
  if (!rows.length) return;
  $('rankingBox').style.height = `${Math.max(120, rows.length * 28 + 50)}px`;

  const labels = rows.map((c) => `${c.score === c.total ? '' : '✕ '}${c.indeks}`);
  const data = rows.map((c) => c.duration);
  const colors = rows.map((c) => (c.score === c.total ? css('--s1') : css('--critical')));
  let ch = ui.charts.ranking;
  if (!ch) {
    chartDefaults();
    ch = ui.charts.ranking = new Chart($('rankingChart'), {
      type: 'bar',
      data: { labels, datasets: [{ data, backgroundColor: colors, borderRadius: 4, borderSkipped: 'start', barThickness: 16 }] },
      options: {
        indexAxis: 'y', maintainAspectRatio: false, animation: { duration: 250 },
        plugins: {
          legend: { display: false },
          tooltip: {
            ...tooltipStyle(), displayColors: false,
            callbacks: {
              title: (items) => `Indeks ${ch.$rows[items[0].dataIndex].indeks} · uruchomienie #${ch.$rows[items[0].dataIndex].run}`,
              label: (item) => {
                const c = ch.$rows[item.dataIndex];
                return [`czas: ${c.duration.toFixed(3)} s`, `przetwarzanie: ${fmtSec(c.processing)} s`, `przyspieszenie: ${c.speedup == null ? '–' : '×' + c.speedup.toFixed(2)}`,
                  `poprawność: ${c.score}/${c.total}`, `zdarzeń: ${fmtInt(c.events)}`];
              },
            },
          },
        },
        scales: {
          x: { beginAtZero: true, title: { display: true, text: 'sekundy' }, grid: { color: css('--grid') } },
          y: { grid: { display: false }, ticks: { color: css('--text-2') } },
        },
      },
    });
  } else {
    ch.data.labels = labels;
    ch.data.datasets[0].data = data;
    ch.data.datasets[0].backgroundColor = colors;
    ch.update();
  }
  ch.$rows = rows;
}

// ---------------------------------------------------------------- komunikaty
function matches(m) {
  const dir = $('fDir').value, kind = $('fKind').value, cl = $('fClient').value.trim();
  if (dir && m.direction !== dir) return false;
  if (kind && m.kind !== kind) return false;
  if (cl && !String(m.client ?? '').includes(cl)) return false;
  if ($('fErrors').checked && !(m.status === 0 || m.status >= 400)) return false;
  return true;
}

function statusCell(m) {
  if (m.status == null) return '<span class="status-wait">…</span>';
  if (m.status === 0) return '<span class="status-bad">✕ brak połączenia</span>';
  return m.status >= 400 ? `<span class="status-bad">✕ ${m.status}</span>` : `<span class="status-ok">${m.status}</span>`;
}

function logRow(m) {
  const tr = document.createElement('tr');
  tr.className = 'row';
  tr.dataset.id = m.id;
  tr.innerHTML = logCells(m);
  return tr;
}

function logCells(m) {
  return `<td class="mono">${fmtTime(m.ts)}</td>
    <td class="dir" title="${m.direction === 'in' ? 'do serwera' : 'od serwera do klienta'}">${m.direction === 'in' ? '→' : '←'}</td>
    <td>${esc(KIND[m.kind] || m.kind)}</td>
    <td>${esc(m.client ?? '–')}</td>
    <td class="mono path" title="${esc(m.path)}">${esc(m.path)}</td>
    <td>${statusCell(m)}</td>
    <td class="num">${fmtSize(m.size)}</td>
    <td>${esc(m.summary)}</td>`;
}

function patchLogRow(m) {
  const tr = $('logBody').querySelector(`tr.row[data-id="${m.id}"]`);
  if (tr) tr.innerHTML = logCells(m);
}

function removeLogRow(tr) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains('body-row')) next.remove();
  tr.remove();
}

function renderLog() {
  const body = $('logBody');
  const list = ui.messages.filter(matches);
  if ($('fFollow').checked) list.reverse();
  body.replaceChildren();
  for (const m of list) {
    body.append(logRow(m));
    if (ui.openBodies.has(m.id)) body.append(bodyRow(m.id));
  }
  $('logEmpty').hidden = list.length > 0;
}

function bodyRow(id) {
  const tr = document.createElement('tr');
  tr.className = 'body-row';
  tr.innerHTML = '<td colspan="8"><pre class="json">wczytywanie…</pre></td>';
  const pre = tr.querySelector('pre');
  const show = (b) => { pre.textContent = JSON.stringify(b, null, 2); };
  if (ui.bodies.has(id)) show(ui.bodies.get(id));
  else api(`/api/messages/${id}`).then((r) => { ui.bodies.set(id, r.body); show(r.body); })
    .catch((e) => { pre.textContent = e.message; });
  return tr;
}

function toggleBody(tr) {
  const id = parseInt(tr.dataset.id, 10);
  const next = tr.nextElementSibling;
  if (next && next.classList.contains('body-row')) {
    next.remove();
    ui.openBodies.delete(id);
  } else {
    tr.after(bodyRow(id));
    ui.openBodies.add(id);
  }
}

// ---------------------------------------------------------------- szczegóły klienta
async function openDetail(indeks) {
  ui.detail = indeks;
  $('detailTitle').textContent = `Klient ${indeks}`;
  $('detail').showModal();
  await refreshDetail();
}

async function refreshDetail() {
  const indeks = ui.detail;
  let data;
  try { data = await api(`/api/clients/${indeks}/comparison`); } catch (e) {
    $('detailSummary').textContent = e.message; return;
  }
  const c = data.client, run = data.run;
  $('detailSummary').innerHTML = [
    ['Adres', `${esc(c.ip_addr)}:${c.port}`], ['Status', statusBadge(c)],
    ['Eksperyment', run ? `#${run.id} ${esc(run.variant || 'ręczny')}` : '–'], ['Zdarzeń', fmtInt(c.events || null)],
    ['Czas całkowity', c.duration == null ? '–' : `${c.duration.toFixed(3)} s`],
    ['Transfer danych', c.transfer == null ? '–' : `${c.transfer.toFixed(3)} s`],
    ['Przetwarzanie', c.result_before_ack && c.status === 'done' ? '<span class="warn">⚠ wynik przed potwierdzeniem odbioru</span>' : (c.processing == null ? '–' : `${c.processing.toFixed(3)} s`)],
    ['Wzorzec (przetwarzanie)', run && run.reference_status === 'done' ? `${run.reference_processing.toFixed(3)} s` : (run ? refCell(run) : '–')],
    ['Przyspieszenie', c.speedup == null ? '–' : `×${c.speedup.toFixed(2)}`],
    ['Poprawność', c.score == null ? '–' : `${c.score}/${c.total}`],
  ].map(([k, v]) => `<span>${k}: <b>${v}</b></span>`).join('');

  renderHistory(c, data);
  renderDifferences(data);
  renderComparison(data);
}

function renderDifferences(data) {
  const cmp = data.comparison;
  if (!cmp) {
    $('diffInfo').textContent = '';
    $('diffWrap').innerHTML = `<p class="muted">${data.reference ? 'Oczekiwanie na wynik klienta.' : 'Wzorzec jeszcze nie skończył albo klient nie dostał danych.'}</p>`;
    return;
  }
  const missing = cmp.filter((r) => r.missing).map((r) => r.day);
  const diffs = cmp.flatMap((r) => (r.missing ? [] : Object.entries(r.values).filter(([, v]) => !v.ok)
    .map(([field, v]) => ({ day: r.day, field, ...v }))));
  $('diffInfo').textContent = `${diffs.length} błędnych wartości` + (missing.length ? ` · brakujące dni: ${missing.length}` : '');
  if (!diffs.length && !missing.length) {
    $('diffWrap').innerHTML = '<p class="ok-note">✓ Wszystkie wartości zgodne ze wzorcem.</p>';
    return;
  }
  let html = missing.length ? `<p class="muted">Brakujące dni w odpowiedzi: ${missing.slice(0, 40).join(', ')}${missing.length > 40 ? '…' : ''}</p>` : '';
  if (diffs.length) {
    html += '<table class="diffs"><thead><tr><th class="num">Dzień</th><th>Wartość</th><th class="num">Klient</th><th class="num">Wzorzec</th><th class="num">Różnica</th></tr></thead><tbody>' +
      diffs.slice(0, 500).map((d) => `<tr><td class="num">${d.day}</td><td class="mono">${d.field}</td><td class="num">${d.client}</td><td class="num">${d.server}</td>
        <td class="num bad">${d.diff > 0 ? '+' : ''}${Number(d.diff.toFixed(4))}</td></tr>`).join('') + '</tbody></table>';
    if (diffs.length > 500) html += `<p class="muted">pokazano 500 z ${diffs.length}</p>`;
  }
  $('diffWrap').innerHTML = html;
}

function renderHistory(c, data) {
  const hist = c.history;
  const refTimes = new Map((ui.snap ? ui.snap.runs : []).map((r) => [r.id, r.reference_processing]));
  const labels = hist.map((h) => `#${h.run} ${h.variant || 'ręczny'}`);
  const datasets = [
    { label: `klient ${c.indeks} – przetwarzanie`, data: hist.map((h) => h.processing ?? h.duration), borderColor: css('--s1'), backgroundColor: css('--s1'),
      pointBackgroundColor: hist.map((h) => (h.score === h.total ? css('--s1') : css('--critical'))) },
    { label: 'wzorzec sekwencyjny', data: hist.map((h) => refTimes.get(h.run) ?? null), borderColor: css('--s2'), backgroundColor: css('--s2'),
      borderDash: [5, 4] },
  ].map((d) => ({ borderWidth: 2, pointRadius: 4, pointHoverRadius: 6, pointBorderColor: css('--surface'), pointBorderWidth: 2, tension: 0, ...d }));
  let ch = ui.charts.hist;
  if (!ch) {
    chartDefaults();
    ch = ui.charts.hist = new Chart($('histChart'), {
      type: 'line',
      data: { labels, datasets },
      options: {
        maintainAspectRatio: false, animation: false, interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 10, boxHeight: 10, color: css('--text-2') } },
          tooltip: {
            ...tooltipStyle(),
            callbacks: {
              title: (items) => `Eksperyment ${items[0].label}`,
              label: (item) => ` ${item.dataset.label}: ${item.parsed.y == null ? '–' : item.parsed.y.toFixed(3) + ' s'}`,
              afterBody: (items) => {
                const h = ch.$hist[items[0].dataIndex];
                return [`czas całkowity: ${h.duration.toFixed(3)} s`, `poprawność: ${h.score}/${h.total}`, `przyspieszenie: ${h.speedup ? '×' + h.speedup.toFixed(2) : '–'}`];
              },
            },
          },
        },
        scales: { y: { beginAtZero: true, title: { display: true, text: 'sekundy' } }, x: { grid: { display: false } } },
      },
    });
  } else {
    ch.data.labels = labels;
    ch.data.datasets = datasets;
    ch.update();
  }
  ch.$hist = hist;
}

function renderComparison(data) {
  const parks = ui.config.parkings, types = ui.config.aggregate_types;
  const short = { ENTRIES: 'wjazdy', REJECTED: 'odbite', MAX_OCCUPANCY: 'max', REVENUE: 'przychód', AVG_STAY: 'śr. post.', MEDIAN_STAY: 'mediana' };
  if (!data.reference) { $('cmpWrap').innerHTML = '<p class="empty">Klient nie dostał jeszcze danych.</p>'; return; }
  const cmp = data.comparison;
  let html = '<table class="cmp"><thead><tr><th rowspan="2">dzień</th>' +
    parks.map((p) => `<th class="group" colspan="${types.length}">${p}</th>`).join('') + '</tr><tr>' +
    parks.map(() => types.map((t) => `<th>${short[t] || t}</th>`).join('')).join('') + '</tr></thead><tbody>';
  data.reference.forEach((ref, d) => {
    const row = cmp && cmp[d];
    html += `<tr class="${row && row.missing ? 'missing' : ''}"><td class="day">${ref.day}${row && row.missing ? ' (brak)' : ''}</td>`;
    for (const p of parks) {
      for (const t of types) {
        const key = `${p}_${t}`;
        if (!row) { html += `<td class="muted">${fmtVal(ref[key], t)}</td>`; continue; }
        const v = row.values[key];
        html += `<td class="${v.ok ? '' : 'bad'}" data-tip="${esc(`${key}, dzień ${ref.day}\nklient: ${v.client ?? 'brak'}\nwzorzec: ${v.server}${v.diff ? `\nróżnica: ${v.diff > 0 ? '+' : ''}${v.diff}` : ''}`)}">${v.client == null ? '–' : fmtVal(v.client, t)}</td>`;
      }
    }
    html += '</tr>';
  });
  html += '</tbody></table>';
  if (!cmp) html = '<p class="muted">Oczekiwanie na wynik klienta – poniżej wartości referencyjne.</p>' + html;
  $('cmpWrap').innerHTML = html;
}

const fmtVal = (v, t) => (t === 'REVENUE' ? Number(v).toFixed(2) : Number.isInteger(v) ? v : Number(v).toFixed(2));

// ---------------------------------------------------------------- zdarzenia UI
function bindEvents() {
  $('startForm').addEventListener('submit', (e) => {
    e.preventDefault();
    startRun(targetClients());
  });
  $('variants').addEventListener('click', (e) => {
    const b = e.target.closest('.variant');
    if (b && !b.disabled) startRun(targetClients(), b.dataset.variant);
  });
  $('runsBody').addEventListener('click', async (e) => {
    if (e.target.dataset.act !== 'del-run') return;
    const id = e.target.closest('tr').dataset.run;
    if (!confirm(`Usunąć eksperyment #${id}? Jego wyniki znikną z historii i rankingu.`)) return;
    await api(`/api/runs/${id}`, { method: 'DELETE' }).catch((err) => alert(err.message));
  });
  $('target').addEventListener('change', renderStartState);

  $('clientsBody').addEventListener('click', async (e) => {
    const tr = e.target.closest('tr');
    if (!tr) return;
    const indeks = parseInt(tr.dataset.indeks, 10);
    if (e.target.classList.contains('sel')) {
      if (e.target.checked) ui.selected.add(indeks); else ui.selected.delete(indeks);
      renderStartState();
      $('clientsInfo').textContent = `${ui.snap.clients.length} zarejestrowanych · zaznaczonych: ${ui.selected.size}`;
      $('selectAll').checked = ui.selected.size === ui.snap.clients.length;
      return;
    }
    const act = e.target.dataset.act;
    if (act === 'detail') openDetail(indeks);
    if (act === 'remove' && confirm(`Usunąć klienta ${indeks}?`)) {
      await api(`/api/clients/${indeks}`, { method: 'DELETE' }).catch(() => {});
    }
  });
  $('selectAll').addEventListener('change', (e) => {
    ui.selected = new Set(e.target.checked ? ui.snap.clients.map((c) => c.indeks) : []);
    renderClients();
    renderStartState();
  });

  for (const id of ['fDir', 'fKind', 'fErrors', 'fFollow']) $(id).addEventListener('change', renderLog);
  $('fClient').addEventListener('input', renderLog);
  $('logBody').addEventListener('click', (e) => {
    const tr = e.target.closest('tr.row');
    if (tr) toggleBody(tr);
  });
  $('clearLog').addEventListener('click', async () => {
    await api('/api/messages', { method: 'DELETE' }).catch(() => {});
    ui.messages = [];
    ui.openBodies.clear();
    ui.bodies.clear();
    renderLog();
  });

  $('detailClose').addEventListener('click', () => $('detail').close());
  $('detail').addEventListener('close', () => { ui.detail = null; ui.detailSig = null; });

  // podpowiedzi w tabeli porównania
  const tip = $('tooltip');
  $('cmpWrap').addEventListener('mousemove', (e) => {
    const td = e.target.closest('td[data-tip]');
    if (!td) { tip.style.opacity = 0; return; }
    tip.innerText = td.dataset.tip;
    tip.style.left = `${Math.min(e.clientX + 12, innerWidth - tip.offsetWidth - 8)}px`;
    tip.style.top = `${e.clientY + 14}px`;
    tip.style.opacity = 1;
  });
  $('cmpWrap').addEventListener('mouseleave', () => { tip.style.opacity = 0; });
}

init();
