from datetime import datetime
from pathlib import Path
import html


def esc(value):
    return html.escape(str(value))


def badge_class(level):
    level = str(level).lower()

    if level in ("high", "critical"):
        return "danger"

    if level in ("medium", "warning"):
        return "warning"

    if level in ("low", "ok", "good"):
        return "success"

    return "neutral"


def generate_html_report(report_data):

    security = report_data.get("security_score", {})
    system = report_data.get("system", {})
    resources = report_data.get("resources", {})
    battery = report_data.get("battery", {})
    health = report_data.get("health", {})
    firewall = report_data.get("firewall", {})
    ports = report_data.get("ports", {})
    processes = report_data.get("processes", {})
    process_analysis = report_data.get("process_analysis", {})
    connections = report_data.get("connections", {})
    log_analysis = report_data.get("log_analysis", {})

    score = security.get("score", 0)
    status = str(security.get("status", "UNKNOWN")).upper()

    issues = security.get("issues", [])

    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    for issue in issues:

        level = issue.get(
            "level",
            ""
        ).upper()

        if level == "CRITICAL":
            critical_count += 1

        elif level == "HIGH":
            high_count += 1

        elif level == "MEDIUM":
            medium_count += 1

        elif level == "LOW":
            low_count += 1
    suspicious = process_analysis.get("suspicious", [])
    connection_findings = connections.get("findings", [])
    failed_attempts = log_analysis.get("failed_attempts", [])
    process_list = processes.get("top_processes", [])

    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if status == "GOOD":
        score_class = "success"
    elif status == "WARNING":
        score_class = "warning"
    else:
        score_class = "danger"

    firewall_status = str(
        firewall.get("firewall", "Unknown")
    ).upper()

    if firewall_status == "ENABLED":
        firewall_badge = "success"
    else:
        firewall_badge = "danger"

    html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Cross-Platform Triage SOC Dashboard</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    background: #0b1120;
    color: #e5e7eb;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
}}

.container {{
    max-width: 1450px;
    margin: auto;
    padding: 30px;
}}

/* HEADER */

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}}

.header h1 {{
    margin: 0;
    font-size: 28px;
    color: #f8fafc;
}}

.header p {{
    margin: 7px 0 0;
    color: #94a3b8;
    font-size: 14px;
}}

.header-right {{
    text-align: right;
    color: #64748b;
    font-size: 13px;
}}

/* GRID */

.grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}}

.two-column {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}}

@media (max-width: 900px) {{
    .two-column {{
        grid-template-columns: 1fr;
    }}
}}

/* CARDS */

.card {{
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 18px;
}}

.card-title {{
    font-size: 16px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 18px;
}}

.metric {{
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 18px;
}}

.metric-label {{
    color: #64748b;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}}

.metric-value {{
    margin-top: 8px;
    color: #f8fafc;
    font-size: 24px;
    font-weight: 700;
}}

/* SCORE */

.score-card {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.score-number {{
    font-size: 58px;
    font-weight: 800;
    line-height: 1;
}}

.score-label {{
    margin-top: 10px;
    font-size: 13px;
    color: #64748b;
}}

.status {{
    display: inline-block;
    margin-top: 12px;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

/* COLORS */

.success {{
    color: #22c55e;
}}

.warning {{
    color: #f59e0b;
}}

.danger {{
    color: #ef4444;
}}

.neutral {{
    color: #94a3b8;
}}

.status.success {{
    background: rgba(34,197,94,0.12);
}}

.status.warning {{
    background: rgba(245,158,11,0.12);
}}

.status.danger {{
    background: rgba(239,68,68,0.12);
}}

/* TABLE */

.table-container {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    padding: 11px 12px;
    text-align: left;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    background: #0f172a;
}}

td {{
    padding: 12px;
    border-top: 1px solid #1e293b;
    font-size: 13px;
    color: #cbd5e1;
}}

tr:hover {{
    background: #0f172a;
}}

/* BADGES */

.badge {{
    display: inline-block;
    padding: 5px 9px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
}}

.badge.success {{
    background: rgba(34,197,94,0.12);
    color: #22c55e;
}}

.badge.warning {{
    background: rgba(245,158,11,0.12);
    color: #f59e0b;
}}

.badge.danger {{
    background: rgba(239,68,68,0.12);
    color: #ef4444;
}}

.badge.neutral {{
    background: rgba(148,163,184,0.12);
    color: #94a3b8;
}}

/* FINDINGS */

.finding {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 13px 0;
    border-bottom: 1px solid #1e293b;
}}

.finding:last-child {{
    border-bottom: none;
}}

.severity {{
    min-width: 65px;
    text-align: center;
    padding: 5px 8px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
}}

.severity-high {{
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
}}

.severity-medium {{
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
}}

.severity-low {{
    background: rgba(34, 197, 94, 0.12);
    color: #22c55e;
}}

.finding-text {{
    color: #cbd5e1;
    font-size: 13px;
    line-height: 1.5;
}}

/* EMPTY */

.empty {{
    color: #64748b;
    font-size: 13px;
    padding: 10px 0;
}}

/* FOOTER */

.footer {{
    text-align: center;
    padding: 25px 0 10px;
    color: #475569;
    font-size: 12px;
}}

</style>

</head>

<body>

<div class="container">

<!-- HEADER -->

<div class="header">

<div>

<h1>Cross-Platform Triage Tool</h1>

<p>SOC Security Dashboard</p>

</div>

<div class="header-right">

<div>{esc(generated_at)}</div>

<div>{esc(system.get("hostname", "Unknown"))}</div>

</div>

</div>


<!-- OVERVIEW -->

<div class="grid">

<div class="card score-card">

<div>

<div class="metric-label">

Security Score
</div>

<div class="score-number {score_class}">
{esc(score)}/100
</div>

<div class="status {score_class}">
{esc(status)}
</div>

</div>

</div>


<div class="metric">

<div class="metric-label">
Security Findings
</div>

<div class="metric-value">
{len(issues)}
</div>

</div>


<div class="metric">

<div class="metric-label">
Suspicious Processes
</div>

<div class="metric-value">
{len(suspicious)}
</div>

</div>


<div class="metric">

<div class="metric-label">
Failed Auth Attempts
</div>

<div class="metric-value">
{len(failed_attempts)}
</div>

</div>

</div>

<div class="card">

<div class="card-title">
Alert Severity Summary
</div>


<div class="severity-grid">


<div class="severity-card">

<div class="severity-title">
CRITICAL
</div>

<div class="severity-number critical-text">
{critical_count}
</div>

</div>


<div class="severity-card">

<div class="severity-title">
HIGH
</div>

<div class="severity-number high-text">
{high_count}
</div>

</div>


<div class="severity-card">

<div class="severity-title">
MEDIUM
</div>

<div class="severity-number medium-text">
{medium_count}
</div>

</div>


<div class="severity-card">

<div class="severity-title">
LOW
</div>

<div class="severity-number low-text">
{low_count}
</div>

</div>


</div>

</div>

<!-- SYSTEM -->

<div class="card">

<div class="card-title">

System Information
</div>

<div class="grid">

<div class="metric">

<div class="metric-label">
Hostname
</div>

<div class="metric-value">
{esc(system.get("hostname", "Unknown"))}
</div>

</div>


<div class="metric">

<div class="metric-label">
Operating System
</div>

<div class="metric-value">
{esc(system.get("system", "Unknown"))}
</div>

</div>


<div class="metric">

<div class="metric-label">
Release
</div>

<div class="metric-value">
{esc(system.get("release", "Unknown"))}
</div>

</div>


<div class="metric">

<div class="metric-label">
Architecture
</div>

<div class="metric-value">
{esc(system.get("architecture", "Unknown"))}
</div>

</div>

</div>

</div>


<!-- RESOURCES -->

<div class="card">

<div class="card-title">
System Resources
</div>

<div class="grid">

<div class="metric">

<div class="metric-label">
Memory
</div>

<div class="metric-value">
{esc(resources.get("memory", {}).get("percent", 0))}%
</div>

</div>


<div class="metric">

<div class="metric-label">
Disk
</div>

<div class="metric-value">
{esc(resources.get("disk", {}).get("percent", 0))}%
</div>

</div>


<div class="metric">

<div class="metric-label">
Battery
</div>

<div class="metric-value">
{esc(battery.get("percent", "Unknown"))}%
</div>

</div>


<div class="metric">

<div class="metric-label">
Health
</div>

<div class="metric-value">
{esc(health.get("status", "Unknown")).upper()}
</div>

</div>

</div>

</div>


<!-- FINDINGS -->

<div class="card">

<div class="card-title">
Security Findings
</div>
"""

    if issues:

        for issue in issues:

            issue_text = str(issue)

            if "Firewall disabled" in issue_text:
                severity = "HIGH"

            elif "High-risk" in issue_text:
                severity = "HIGH"

            elif "SSH" in issue_text:
                severity = "MEDIUM"

            elif "Open port" in issue_text:
                severity = "MEDIUM"

            else:
                severity = "LOW"

            html_content += f"""
    <div class="finding">

    <span class="severity severity-{severity.lower()}">
    {severity}
    </span>

    <div class="finding-text">
    {esc(issue_text)}
    </div>

    </div>
    """

    else:

        html_content += """
    <div class="finding">

    <span class="severity severity-low">
    OK
    </span>

    <div class="finding-text">
    No security issues detected.
    </div>

    </div>
    """

    html_content += f"""

</div>


<!-- FIREWALL + PORTS -->

<div class="two-column">

<div class="card">

<div class="card-title">
Firewall Status
</div>

<div class="metric">

<div class="metric-label">
Firewall
</div>

<div style="margin-top:10px;">

<span class="badge {firewall_badge}">
{esc(firewall_status)}
</span>

</div>

</div>

</div>


<div class="card">

<div class="card-title">
Open Ports
</div>

<div class="table-container">

<table>

<tr>
<th>Port</th>
<th>Service</th>
<th>Status</th>
</tr>
"""

    open_ports = ports.get("open_ports", [])

    if open_ports:

        for port in open_ports:

            html_content += f"""
<tr>

<td>{esc(port.get("port", ""))}</td>

<td>{esc(port.get("service", ""))}</td>

<td>
<span class="badge neutral">
{esc(port.get("status", "OPEN"))}
</span>
</td>

</tr>
"""

    else:

        html_content += """
<tr>
<td colspan="3">
No open ports detected.
</td>
</tr>
"""

    html_content += """

</table>

</div>

</div>

</div>


<!-- PROCESS ANALYSIS -->

<div class="card">

<div class="card-title">
Suspicious Process Analysis
</div>

<div class="table-container">

<table>

<tr>
<th>PID</th>
<th>Process</th>
<th>Executable</th>
<th>Risk</th>
<th>Reason</th>
</tr>
"""

    if suspicious:

        for process in suspicious:

            reasons = process.get("reason", [])

            if isinstance(reasons, list):

                reasons = ", ".join(reasons)

            html_content += f"""
<tr>

<td>{esc(process.get("pid", ""))}</td>

<td>{esc(process.get("name", ""))}</td>

<td>{esc(process.get("exe", ""))}</td>

<td>
<span class="badge danger">
HIGH
</span>
</td>

<td>{esc(reasons)}</td>

</tr>
"""

    else:

        html_content += """
<tr>
<td colspan="5">
No suspicious processes detected.
</td>
</tr>
"""

    html_content += """

</table>

</div>

</div>


<!-- NETWORK CONNECTIONS -->

<div class="card">

<div class="card-title">
Network Connection Findings
</div>

<div class="table-container">

<table>

<tr>
<th>Level</th>
<th>Process</th>
<th>PID</th>
<th>Message</th>
</tr>
"""

    if connection_findings:

        for finding in connection_findings:

            level = str(
                finding.get("level", "UNKNOWN")
            ).upper()

            level_class = badge_class(level)

            html_content += f"""
<tr>

<td>
<span class="badge {level_class}">
{esc(level)}
</span>
</td>

<td>{esc(finding.get("process", ""))}</td>

<td>{esc(finding.get("pid", ""))}</td>

<td>{esc(finding.get("message", ""))}</td>

</tr>
"""

    else:

        html_content += """
<tr>
<td colspan="4">
No network findings detected.
</td>
</tr>
"""

    html_content += """

</table>

</div>

</div>


<!-- LOG ANALYSIS -->

<div class="card">

<div class="card-title">
Authentication Log Analysis
</div>
"""

    if failed_attempts:

        html_content += f"""
<div class="metric">

<div class="metric-label">
Failed Authentication Attempts
</div>

<div class="metric-value danger">
{len(failed_attempts)}
</div>

</div>

<br>

<div class="table-container">

<table>

<tr>
<th>#</th>
<th>Event</th>
</tr>
"""

        for index, attempt in enumerate(
            failed_attempts,
            start=1
        ):

            html_content += f"""
<tr>

<td>{index}</td>

<td>{esc(attempt)}</td>

</tr>
"""

        html_content += """

</table>

</div>
"""

    else:

        html_content += """
<div class="metric">

<div class="metric-label">
Authentication Status
</div>

<div class="metric-value success">
OK
</div>

</div>

<p class="empty">
No failed authentication attempts detected.
</p>
"""

    html_content += """

</div>


<!-- TOP PROCESSES -->

<div class="card">

<div class="card-title">
Top Processes
</div>

<div class="table-container">

<table>

<tr>
<th>PID</th>
<th>Process</th>
<th>CPU</th>
<th>Memory</th>
<th>User</th>
</tr>
"""

    if process_list:

        for process in process_list:

            cpu = process.get("cpu", 0)
            memory = process.get("memory", 0)

            html_content += f"""
<tr>

<td>{esc(process.get("pid", ""))}</td>

<td>{esc(process.get("name", ""))}</td>

<td>{round(float(cpu), 2)}%</td>

<td>{round(float(memory), 2)}%</td>

<td>{esc(process.get("user", ""))}</td>

</tr>
"""

    else:

        html_content += """
<tr>
<td colspan="5">
No process information available.
</td>
</tr>
"""

    html_content += """

</table>

</div>

</div>


<!-- FOOTER -->

<div class="footer">

Cross-Platform Triage Tool
&nbsp;•&nbsp;
SOC-style security report
&nbsp;•&nbsp;
Generated automatically

</div>


</div>

</body>

</html>
"""

    return html_content


def save_html_report(report_data):

    reports_dir = Path("reports")

    reports_dir.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = (
        reports_dir
        / f"triage_report_{timestamp}.html"
    )

    html_content = generate_html_report(
        report_data
    )

    file_path.write_text(
        html_content,
        encoding="utf-8"
    )

    return str(file_path)