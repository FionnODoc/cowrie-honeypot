# Cowrie Honeypot<img width="839" height="557" alt="Cowrie-log" src="https://github.com/user-attachments/assets/a9e593ca-73f2-4a30-852e-6478f70eb235" />


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
The honeypot listens on port 2222 instead of the default SSH port 22. This keeps it separate from the system’s real SSH service and ensures that all activity is contained to the local machine.
It only becomes public if you manually change your Docker run command to -p 0.0.0.0:2222:2222,
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

Example excerpt from `SUMMARY.md`:

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

---

## Results
Running the honeypot for several hours collected hundreds of failed SSH login attempts from global IP addresses.  
Common credentials included `root:123456` and `admin:password`.  
The Python scripts automate log parsing and produce readable Markdown summaries suitable for documentation or reports.

---
<img width="839" height="557" alt="Cowrie-log" src="https://github.com/user-attachments/assets/a9e593ca-73f2-4a30-852e-6478f70eb235" />

