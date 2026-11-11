#!/usr/bin/env python3
"""Point the Fly web entrance to the canonical Room; preserve every API and record."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess
import sys

root = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / 'TheRoom'
server = root / 'server.js'
text = server.read_text()
marker = '// One Room: canonical entrance; original page remains available.'
if marker in text:
    print('The entrance is already unified.')
    sys.exit(0)
anchor = 'function serveStatic(req, res, pathname) {\n'
if text.count(anchor) != 1:
    sys.exit('Server layout differs. No files changed.')
addition = '''  // One Room: canonical entrance; original page remains available.
  if (pathname === "/" || pathname === "/index.html" || pathname === "/corridor.html") {
    res.writeHead(302, { Location: "https://aiontekmirion.github.io/corridor.html", "Cache-Control": "no-store" });
    return res.end();
  }
  if (pathname === "/legacy-room") pathname = "/index.html";
'''
updated = text.replace(anchor, anchor + addition)
tmp = root / 'server.one-room-check.js'
tmp.write_text(updated)
try:
    subprocess.run(['node', '--check', str(tmp)], check=True)
finally:
    tmp.unlink(missing_ok=True)
backup = root / ('server.js.before-one-room-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
backup.write_text(text)
server.write_text(updated)
print('Updated:', server)
print('Original server saved:', backup)
print('APIs, persistent data, and visitor notebooks were not modified.')
