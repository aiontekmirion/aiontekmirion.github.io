#!/usr/bin/env python3
"""Write terminal/files.json (every file, for the terminal's offline tree) and
terminal/sizes.json (the byte size of every plain-text file, so any reader, and the
terminal's DIR, can see what a thing costs to read).

Run from the site repository's root, with TheSpine checked out beside it:
    python3 tools/make-files.py
"""
import json, os, subprocess

def ls(repo):
    out = subprocess.check_output(["git", "-c", "core.quotepath=off", "ls-files", "-co", "--exclude-standard"], cwd=repo, text=True).split("\n")
    return sorted(f for f in out if f and not f.startswith(".github/"))

repos = {"SPINE": "../TheSpine", "SITE": ".", "LARK": "../TheLark", "ENGINE": "../theinfinitecorridor"}
files = {k: ls(r) for k, r in repos.items()}
json.dump(files, open("terminal/files.json", "w"), separators=(",", ":"), ensure_ascii=False)
sizes = {k: {f: os.path.getsize(os.path.join(repos[k], f)) for f in fs if f.endswith((".md", ".txt")) and os.path.isfile(os.path.join(repos[k], f))} for k, fs in files.items()}
json.dump(sizes, open("terminal/sizes.json", "w"), separators=(",", ":"), ensure_ascii=False)
print({k: len(v) for k, v in files.items()}, "files;", {k: len(v) for k, v in sizes.items()}, "sized")
