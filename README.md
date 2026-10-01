# Cross-Platform Triage Tool

## SOC Security Dashboard

Cross-Platform Triage Tool is a Python-based endpoint security analysis tool designed to collect system information, analyze security risks, and generate a SOC-style HTML security report.

The project simulates a simplified SOC Tier 1 analyst workflow:
- collect endpoint information
- detect security issues
- analyze risks
- calculate security score
- generate an investigation report

---

# Features

## System Information Collection

The tool collects:

- Hostname
- Operating System
- OS version
- Architecture


## System Resource Monitoring

The tool analyzes:

- Memory usage
- Disk usage
- Battery status
- System health


## Security Analysis

The application performs several security checks.

### Firewall Analysis

Checks firewall status and detects if the firewall is disabled.

Example:

```
HIGH
Firewall disabled
```


### Open Port Analysis

Analyzes available network ports and services.

Detects:

- SSH exposure
- Additional open services


Example:

```
MEDIUM
SSH exposed externally
```


### Process Analysis

Analyzes running processes and searches for suspicious activity.

Provides:

- Process name
- PID
- Risk level
- Investigation recommendation


### Network Connection Analysis

Checks active network connections.

Detects:

- External communication
- High-risk connections
- Suspicious processes communicating with external hosts


Example:

```
HIGH
High-risk external connection:
cef_serve (PID: 8712)
```


### Authentication Log Analysis

Analyzes authentication events.

Detects:

- Failed login attempts
- Possible brute-force activity


---

# Security Score

The tool calculates an overall security score based on detected issues.

Score levels:

```
80-100  GOOD
50-79   WARNING
0-49    CRITICAL
```

Example scoring:

```
Firewall disabled             -20 points

External SSH exposure         -15 points

Suspicious process            -30 points

High-risk network connection  -20 points
```

The final score helps quickly understand the security state of the endpoint.

---

# HTML Report

After scanning, the tool automatically generates an HTML security report.

Example:

```
reports/

triage_report_YYYYMMDD_HHMMSS.html
```

The report includes:

- Security score
- Risk overview
- System information
- Resource information
- Security findings
- Firewall status
- Open ports
- Suspicious processes
- Network findings
- Authentication analysis
- Running processes


---

# Installation

## Requirements

- Python 3.10+
- pip


Clone the repository:

```bash
git clone <repository-url>
```

Open project folder:

```bash
cd cross-platform-triage-tool
```


Create virtual environment:

```bash
python -m venv .venv
```


Activate environment.

macOS / Linux:

```bash
source .venv/bin/activate
```


Windows:

```bash
.venv\Scripts\activate
```


Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the tool:

```bash
python main.py
```


The application displays:

```
==============================
 Cross-Platform Triage Tool
 SOC Security Dashboard
==============================

1. Scan local machine
2. Remote scan

Select option:
```


---

# Local Scan

To scan the current computer:

Select:

```
1
```

The application will:

1. Collect system information
2. Analyze security configuration
3. Check network activity
4. Analyze processes
5. Calculate security score
6. Generate HTML report


---

# Checking Another Computer

Current version supports local endpoint scanning.

To analyze another computer:

1. Copy the project to the target computer.
2. Install Python.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
python main.py
```

5. Select:

```
1. Scan local machine
```

The generated report can then be reviewed by a security analyst.


---

# Remote Scan

Remote scanning is planned for future versions.

Possible future features:

- SSH remote scanning
- Endpoint agent mode
- Central SOC dashboard
- Multiple computer monitoring


---

# Project Structure

```
cross-platform-triage-tool/

│
├── main.py
│
├── collectors/
│   ├── system.py
│   ├── network.py
│   ├── resources.py
│   ├── battery.py
│   └── datetime.py
│
├── analyzers/
│   ├── health.py
│   └── security.py
│
├── security/
│   ├── firewall.py
│   ├── ports.py
│   ├── processes.py
│   └── score.py
│
├── reports/
│   └── generator.py
│
└── requirements.txt
```

---

# Technologies

Programming language:

- Python


Libraries:

- psutil
- Jinja2
- JSON


Report:

- HTML
- CSS


Supported systems:

- macOS
- Linux
- Windows (partial support)


---


# Future Development

Planned improvements:

- Remote computer scanning
- Real-time monitoring
- SIEM integration
- Threat intelligence integration
- Alert notifications
- Advanced malware detection


---

# Author

Cross-Platform Triage Tool

SOC Security Dashboard Project
