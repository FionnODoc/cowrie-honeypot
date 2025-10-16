#!/usr/bin/env python3
import json, collections, sys
from pathlib import Path

LOGFILE = sys.argv[1] if len(sys.argv) > 1 else "logs/cowrie.json"
p = Path(LOGFILE)
if not p.exists():
    print(f"Log file {LOGFILE} not found.")
    sys.exit(1)

recs = []
with p.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            pass

ips  = [r.get("src_ip") for r in recs if r.get("src_ip")]
users = [r.get("username") for r in recs if r.get("username")]
pwds  = [r.get("password") for r in recs if r.get("password")]

print("=== Top attacker IPs ===")
for ip, c in collections.Counter(ips).most_common(10):
    print(f"{ip:20} {c:5}")

print("\n=== Top usernames ===")
for u, c in collections.Counter(users).most_common(10):
    print(f"{u:15} {c:5}")

print("\n=== Top passwords ===")
for p, c in collections.Counter(pwds).most_common(10):
    print(f"{p:20} {c:5}")

hours = []
for r in recs:
    t = r.get("timestamp") or r.get("timestamp.iso8601") or r.get("time")
    if t:
        hours.append(t[:13])  
if hours:
    print("\n=== Top hours ===")
    for h, c in collections.Counter(hours).most_common(10):
        print(f"{h} {c}")
