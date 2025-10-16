# Cowrie Honeypot

## Overview
This project sets up a lightweight SSH honeypot using Cowrie inside a Docker container.  
It records failed login attempts, attacker IPs, usernames, and passwords.  
The data is then parsed with Python scripts that generate a Markdown report summarizing attack patterns.

This repository demonstrates practical cybersecurity monitoring, container isolation, and log analysis in a controlled environment.

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/<yourusername>/cowrie-honeypot.git
cd cowrie-honeypot
```

### 2. Start the honeypot
```bash
mkdir -p logs data
docker run -d   --name cowrie-honeypot   -p 2222:2222   -e COWRIE_TELNET_ENABLED=false   -e COWRIE_SSH_LISTEN_PORT=2222   --mount type=bind,src="$PWD/logs",dst=/cowrie/cowrie-git/var/log/cowrie   --mount type=bind,src="$PWD/data",dst=/cowrie/cowrie-git/var/lib/cowrie   cowrie/cowrie
```
On Apple Silicon, add `--platform linux/amd64` after `docker run -d`.

### 3. Generate activity
Connect to the honeypot and type any credentials several times:
```bash
ssh -p 2222 test@127.0.0.1
```
You should see "Permission denied" each time.

### 4. Parse the logs
```bash
python3 parser.py logs/cowrie.json
```

### 5. Create a summary report
```bash
python3 make_summary.py
```
This produces a file named `SUMMARY.md` that lists the top attacker IPs, usernames, passwords, and peak activity hours.

---

## Example Output

Excerpt from `SUMMARY.md`:

| Metric | Count |
| --- | --- |
| Total events | 162 |
| Failed logins | 160 |
| Successful logins | 2 |

| IP | Attempts |
| --- | --- |
| 185.234.219.45 | 43 |
| 37.49.230.19 | 28 |

| Username | Attempts |
| --- | --- |
| root | 89 |
| admin | 36 |
| user | 11 |

---

## Tools Used
| Purpose | Tool |
| --- | --- |
| Containerization | Docker |
| Honeypot | Cowrie |
| Language | Python |
| Reporting | Markdown |
| Operating system | macOS or Linux |

---

## Results
Running the honeypot for several hours collected hundreds of failed SSH login attempts from global IP addresses.  
Common credentials included `root:123456` and `admin:password`.  
The Python scripts automate log parsing and produce readable Markdown summaries suitable for documentation or reports.

---

## Resume Description
Deployed a Dockerized SSH honeypot using Cowrie to collect and analyze brute-force attacks.  
Built Python scripts to summarize attacker IPs, credentials, and activity trends in Markdown format.

---

## Safety Notice
This project is for educational and research use.  
All activity should remain inside the Docker container.  
Do not expose this setup to a production network or systems containing sensitive data.

---

## License
MIT License © 2025  
Author: Fionn O’Dochartaigh
