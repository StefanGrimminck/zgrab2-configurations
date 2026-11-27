#!/usr/bin/env python3
"""Check the repository conventions that CI enforces.

    python3 tools/lint.py

The rules follow CONTRIBUTING.md. The request rules put ZGrab2's own ethics
note into code: probes send only what a standard client would send and never
exploit a vulnerability, so no path traversal, encoded separators, path
parameters, injected arguments, custom headers on CVE probes or raw banner
requests that bypass the HTTP module.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

failures = []


def fail(msg):
    failures.append(msg)


def sections(path):
    secs, module, opts = [], None, {}
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        m = re.match(r"^\[([A-Za-z0-9 ]+)\]\s*$", line)
        if m:
            if module:
                secs.append((module, opts))
            module, opts = m.group(1), {}
            continue
        m = re.match(r"^([a-z0-9-]+)\s*=\s*(.*)$", line.rstrip("\n"))
        if module and m:
            opts[m.group(1)] = m.group(2).strip().strip('"')
        elif module and re.match(r"^[a-z0-9-]+\s*$", line):
            fail(f"{path}:{n}: boolean option without a value, write it as option=true")
    if module:
        secs.append((module, opts))
    return secs


# 1. Plain characters only.
BAD = re.compile("[—→“”‘’]")
for p in ["README.md", "CONTRIBUTING.md"] + glob.glob("**/*.ini", recursive=True):
    for n, line in enumerate(open(p, encoding="utf-8"), 1):
        if BAD.search(line):
            fail(f"{p}:{n}: em-dash, unicode arrow or curly quote (use - and straight quotes)")

probes = sorted(glob.glob("service-discovery/*.ini") + glob.glob("vulnerabilities/*/*.ini"))
cve_files = sorted(glob.glob("vulnerabilities/cve/*.ini"))
# The standard-request rules cover the published folders. A folder added in a
# local overlay gets the format checks only.
STANDARD = ("service-discovery/", "vulnerabilities/misconfigurations/", "vulnerabilities/cve/")
# Headers that the product's own client sends before any login, such as the
# Cisco AnyConnect handshake. Anything else on a CVE probe is a bypass attempt.
CLIENT_HEADERS = {"accept", "accept-language", "x-aggregate-auth", "x-transcend-version"}
names = {}

for p in probes:
    first = open(p, encoding="utf-8").readline()
    # 2. A leading comment that says what the probe finds and what proves a hit.
    if not first.startswith("#"):
        fail(f"{p}: missing leading comment block")
    # 3. CVE probes name their CVE on the first line.
    if p in cve_files and not re.match(r"^# CVE-\d{4}-\d+", first):
        fail(f"{p}: first line must name a CVE as '# CVE-YYYY-NNNNN  -  ...'")

    for module, opts in sections(p):
        name = opts.get("name")
        # 4. name= is lowercase-hyphen and unique.
        if not name or not re.fullmatch(r"[a-z0-9-]+", name):
            fail(f"{p}: name= must be lowercase letters, digits and hyphens")
        elif name in names:
            fail(f"{p}: name {name!r} already used in {names[name]}")
        else:
            names[name] = p
        if "port" not in opts:
            fail(f"{p}: no port=")

        # 5. Standard requests only.
        if not p.startswith(STANDARD):
            continue
        if module == "http":
            ep = opts.get("endpoint")
            if not ep:
                fail(f"{p}: http probe without endpoint=")
                continue
            method = opts.get("method", "GET").upper()
            if method not in ("GET", "HEAD"):
                fail(f"{p}: method {method} - probes only send GET or HEAD")
            low = ep.lower()
            path = low.split("?", 1)[0]
            for bad, why in (("..", "path traversal"), ("%2e", "encoded dot"), ("%2f", "encoded slash"),
                             ("%5c", "encoded backslash"), ("%25", "double encoding"),
                             ("%ad", "argument injection"), ("%00", "null byte"),
                             ("etc/passwd", "system file read"), ("win.ini", "system file read"),
                             ("proc/self", "system file read"), ("file:", "file URL"),
                             ("/@fs/", "file-system route")):
                if bad in low:
                    fail(f"{p}: endpoint contains {bad!r} ({why}); probes may not exploit a vulnerability")
            if ";" in path:
                fail(f"{p}: endpoint path contains ';' (path parameter tricks bypass access checks)")
            if p in cve_files and "custom-headers-names" in opts:
                names_ = {h.strip().lower() for h in opts["custom-headers-names"].split(",")}
                if not names_ <= CLIENT_HEADERS:
                    fail(f"{p}: CVE probes may only send headers a standard client sends "
                         f"({', '.join(sorted(CLIENT_HEADERS))})")
        if module == "banner" and p in cve_files:
            fail(f"{p}: CVE probes may not send raw banner requests")

if failures:
    print("\n".join("FAIL: " + f for f in failures))
    print(f"{len(failures)} convention failure(s)")
    sys.exit(1)
print(f"All conventions hold for {len(probes)} probe configs.")
