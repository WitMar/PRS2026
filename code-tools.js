// Ramki listingów (kod / wynik) z przyciskiem "Kopiuj".
(function () {
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    // Fallback, np. dla stron otwieranych przez http:// bez HTTPS
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand('copy') ? resolve() : reject();
      } catch (e) {
        reject(e);
      } finally {
        document.body.removeChild(ta);
      }
    });
  }

  function wrap(pre) {
    var isCode = pre.classList.contains('code');
    var lang = isCode ? (pre.classList.contains('python') ? 'Python' : 'Kod') : 'Wynik';

    var box = document.createElement('div');
    box.className = 'listing ' + (isCode ? 'listing-code' : 'listing-output');

    var header = document.createElement('div');
    header.className = 'listing-header';
    var label = document.createElement('span');
    label.textContent = lang;
    header.appendChild(label);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = 'Kopiuj';
    btn.title = isCode ? 'Skopiuj kod do schowka' : 'Skopiuj wynik do schowka';
    btn.addEventListener('click', function () {
      var text = pre.textContent.replace(/^\n/, '').replace(/\s+$/, '') + '\n';
      copyText(text).then(function () {
        btn.textContent = 'Skopiowano!';
        btn.classList.add('copied');
      }, function () {
        btn.textContent = 'Błąd kopiowania';
      });
      clearTimeout(btn._t);
      btn._t = setTimeout(function () {
        btn.textContent = 'Kopiuj';
        btn.classList.remove('copied');
      }, 1800);
    });
    header.appendChild(btn);

    pre.parentNode.insertBefore(box, pre);
    box.appendChild(header);
    box.appendChild(pre);
  }

  function init() {
    var blocks = document.querySelectorAll('pre.literal-block');
    for (var i = 0; i < blocks.length; i++) wrap(blocks[i]);

    // Bloki "Zrób to sam!" oznaczamy klasą, nawet jeśli w HTML jej nie ma
    var quotes = document.querySelectorAll('blockquote');
    for (var j = 0; j < quotes.length; j++) {
      var first = quotes[j].querySelector('p');
      if (first && /^\s*Zrób to sam/.test(first.textContent)) {
        quotes[j].classList.add('exercise');
        first.classList.add('exercise-title');
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
