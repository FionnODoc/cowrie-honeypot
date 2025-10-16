#!/usr/bin/env python3
import json, collections, datetime, argparse
from pathlib import Path

def load_records(path: Path):
    if not path.exists():
        print(f"[!] Log file not found: {path}")
        return []
    recs = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except Exception:
                # skip malformed lines
                pass
    return recs

def top_counts(items, n=10):
    return collections.Counter([x for x in items if x]).most_common(n)

def md_table(headers, rows):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser(description="Generate SUMMARY.md from Cowrie JSON logs")
    ap.add_argument("--in", dest="infile", default="logs/cowrie.json", help="Path to cowrie.json")
    ap.add_argument("--out", dest="outfile", default="SUMMARY.md", help="Output markdown file")
    ap.add_argument("--top", dest="topn", type=int, default=10, help="How many rows in top tables")
    args = ap.parse_args()

    log_path = Path(args.infile)
    out_path = Path(args.outfile)

    recs = load_records(log_path)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    total = len(recs)
    failed_logins = sum(1 for r in recs if r.get("eventid") == "cowrie.login.failed")
    successful_logins = sum(1 for r in recs if r.get("eventid") == "cowrie.login.success")
    commands = sum(1 for r in recs if r.get("eventid","").startswith("cowrie.command"))

    ips = [r.get("src_ip") for r in recs]
    usernames = [r.get("username") for r in recs if "username" in r]
    passwords = [r.get("password") for r in recs if "password" in r]

    top_ips = top_counts(ips, args.topn)
    top_users = top_counts(usernames, args.topn)
    top_pwds = top_counts(passwords, args.topn)

    # Hourly summary if timestamps exist
    hours = []
    for r in recs:
        t = r.get("timestamp") or r.get("timestamp.iso8601") or r.get("time")
        if t:
            hours.append(t[:13])  # 2025-10-16T19
    top_hours = top_counts(hours, args.topn)

    md = []
    md.append("# Cowrie Honeypot Summary")
    md.append("")
    md.append(f"_Generated: **{now}** from `{log_path}`_")
    md.append("")
    md.append("## Overview")
    md.append("")
    md.append(md_table(
        ["Metric", "Count"],
        [
            ["Total events", total],
            ["Failed logins", failed_logins],
            ["Successful logins", successful_logins],
            ["Command events", commands],
        ],
    ))
    md.append("")

    md.append("## Top Attacker IPs")
    md.append("")
    md.append(md_table(["IP", "Attempts"], top_ips))
    md.append("")

    md.append("## Top Usernames")
    md.append("")
    md.append(md_table(["Username", "Attempts"], top_users))
    md.append("")

    md.append("## Top Passwords")
    md.append("")
    md.append(md_table(["Password", "Attempts"], top_pwds))
    md.append("")

    if top_hours:
        md.append("## Busiest Hours (UTC)")
        md.append("")
        md.append(md_table(["Hour", "Events"], top_hours))
        md.append("")

    md.append("> Note: This summary is auto-generated from Cowrie JSON logs. It contains no IP geolocation. For GeoIP enrichment, run a separate script or visualize in Kibana/Grafana.")
    md.append("")

    out_path.write_text("\n".join(md), encoding="utf-8")
    print(f"[+] Wrote {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
