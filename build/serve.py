#!/usr/bin/env python3
"""Threaded static server for the generated site. macOS TCC blocks servers from reading ~/Desktop,
so we mirror site/ into the session scratchpad and serve from there (re-synced every request burst)."""
import os, shutil, sys, time, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DST = '/private/tmp/claude-501/-Users-mysense-Desktop/7822ac80-5e0b-490b-9c19-29b6d6d977bd/scratchpad/site_serve'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9711
def sync():
    os.makedirs(DST, exist_ok=True)
    for root, dirs, files in os.walk(SRC):
        rel = os.path.relpath(root, SRC); d = os.path.join(DST, rel); os.makedirs(d, exist_ok=True)
        for f in files:
            s = os.path.join(root, f); t = os.path.join(d, f)
            if not os.path.exists(t) or os.path.getmtime(s) > os.path.getmtime(t): shutil.copy2(s, t)
def syncer():
    while True:
        try: sync()
        except Exception as e: print('sync err', e)
        time.sleep(2)
sync(); threading.Thread(target=syncer, daemon=True).start()
class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=DST, **k)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def log_message(self, *a): pass
print('serving', DST, 'on', PORT, flush=True)
ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
