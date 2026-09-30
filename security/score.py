def calculate_security_score(
    firewall,
    ports,
    process_analysis,
    connections,
    log_analysis
):

    score = 100

    issues = []
    info = []


    # Firewall
    if firewall.get("firewall") == "disabled":
        score -= 20

        issues.append({
            "level": "HIGH",
            "title": "Firewall disabled",
            "impact": "System firewall is not active",
            "score": -20
        })


    # Ports

    open_ports = ports.get(
        "open_ports",
        []
    )


    for port in open_ports:

        port_number = port.get("port")


        if port_number == 22:

            if ports.get("host") == "127.0.0.1":

                info.append(
                    "SSH running locally only"
                )

            else:

                score -= 15

                issues.append({
                    "level": "MEDIUM",

                    "title":
                        "SSH exposed externally",

                    "impact":
                        "Remote access service available",

                    "recommendation":
                        "Restrict SSH access"
                })


        else:

            score -= 10

            issues.append({
                "level": "MEDIUM",
                "title":
                f"Open port {port_number} "
                f"({port.get('service')})",

                "impact":
                "Additional network exposure",

                "recommendation":
                "Review necessity of this service"
            })



    # Processes

    suspicious = process_analysis.get(
        "suspicious",
        []
    )


    for process in suspicious:

        score -= 30

        issues.append({
            "level": "CRITICAL",

            "title":
            f"Suspicious process detected: "
            f"{process.get('name')} "
            f"(PID {process.get('pid')})",

            "impact":
            "Potential malicious activity",

            "recommendation":
            "Investigate process"
        })



    # Network

    findings = connections.get(
        "findings",
        []
    )


    for finding in findings:

        if finding.get("level") == "HIGH":

            score -= 20

            issues.append({
                "level": "HIGH",

                "title":
                f"High-risk external connection: "
                f"{finding.get('process')} "
                f"(PID {finding.get('pid')})",

                "impact":
                "Suspicious external communication",

                "recommendation":
                "Review destination and process"
            })



    # Logs

    failed = log_analysis.get(
        "failed_attempts",
        []
    )


    if len(failed) > 5:

        score -= 10

        issues.append({

            "level": "MEDIUM",

            "title":
            f"Multiple failed login attempts: {len(failed)}",

            "impact":
            "Possible brute-force activity",

            "recommendation":
            "Review authentication logs"

        })



    if score < 0:
        score = 0



    if score >= 80:
        status = "GOOD"

    elif score >= 50:
        status = "WARNING"

    else:
        status = "CRITICAL"



    return {

        "score": score,

        "status": status,

        "issues": issues,

        "info": info

    }