"""Stan serwera współdzielony przez endpointy, wątki wysyłające i panel WWW."""
import json
import threading
import time
from collections import deque

MAX_MESSAGES = 1000
PREVIEW_EVENTS = 25

lock = threading.RLock()
version = 0          # zwiększana przy każdej zmianie - panel odświeża wtedy widok
clients = {}         # indeks -> dict ze stanem klienta
runs = []            # historia uruchomień /start
messages = deque(maxlen=MAX_MESSAGES)
message_updates = deque(maxlen=100)  # zmiany statusu już wysłanych komunikatów
message_bodies = {}  # id -> pełna treść komunikatu (ograniczona do MAX_MESSAGES)
totals = {'messages': 0, 'events_sent': 0, 'results': 0, 'errors': 0}
busy = False
references = {}       # nr eksperymentu -> wynik programu wzorcowego
reference_ready = {}  # nr eksperymentu -> threading.Event (wzorzec skończył)
_next_msg_id = 1


_last_run_id = 0


def next_run_id():
    global _last_run_id
    with lock:
        _last_run_id += 1
        return _last_run_id


def touch():
    global version
    with lock:
        version += 1


def add_message(direction, kind, path, client=None, status=None, body=None, summary=''):
    """Zapisuje komunikat do podglądu w panelu.

    direction: 'in' (do serwera) / 'out' (od serwera do klienta)
    """
    global _next_msg_id
    if isinstance(body, list) and len(body) > PREVIEW_EVENTS:
        body = {'preview': body[:PREVIEW_EVENTS],
                'note': f'pokazano {PREVIEW_EVENTS} z {len(body)} elementów'}
    size = len(json.dumps(body, default=str)) if body is not None else 0
    with lock:
        msg = {'id': _next_msg_id, 'ts': time.time(), 'direction': direction, 'kind': kind,
               'path': path, 'client': client, 'status': status, 'size': size,
               'summary': summary}
        _next_msg_id += 1
        messages.append(msg)
        message_bodies[msg['id']] = body
        while len(message_bodies) > MAX_MESSAGES:
            message_bodies.pop(next(iter(message_bodies)))
        totals['messages'] += 1
        if status is not None and (status >= 400 or status == 0):
            totals['errors'] += 1
        touch()
        return msg


def update_message(msg, **fields):
    with lock:
        msg.update(fields)
        if fields.get('status') is not None and (fields['status'] >= 400 or fields['status'] == 0):
            totals['errors'] += 1
        message_updates.append(dict(msg))
        touch()


def clear_messages():
    with lock:
        messages.clear()
        message_bodies.clear()
        message_updates.clear()
        touch()


def messages_since(last_id):
    with lock:
        return [m for m in messages if m['id'] > last_id]


def new_client(indeks, ip_addr, port):
    return {
        'indeks': indeks, 'ip_addr': ip_addr, 'port': port,
        'registered_at': time.time(),
        'status': 'registered',  # registered/preparing/sending/processing/waiting_reference/done/error
        'run': None, 'variant': None, 'events': 0, 'sent_at': None, 'received_at': None,
        'duration': None, 'speedup': None, 'score': None, 'total': None,
        'n_differences': None, 'error': None, 'source_ip': None,
        'transfer': None, 'processing': None, 'result_before_ack': False,
        'history': [],
        # dane ostatniego uruchomienia (nie wysyłane w snapshot)
        '_comparison': None, '_sent_pc': None, '_ack_pc': None,
    }


def public_client(c):
    return {k: v for k, v in c.items() if not k.startswith('_')}


def snapshot():
    with lock:
        return {
            'version': version,
            'busy': busy,
            'clients': [public_client(c) for c in sorted(clients.values(), key=lambda c: c['indeks'])],
            'runs': list(runs),
            'totals': dict(totals),
            'message_updates': list(message_updates)[-30:],
            'server_time': time.time(),
        }
