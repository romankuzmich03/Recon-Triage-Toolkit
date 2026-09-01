def calculate_security_score(firewall, ports, processes):
    score = 100
    issues = []

    # Firewall
    if firewall.get("firewall") == "disabled":
        score -= 20
        issues.append("Firewall disabled")
    # Open ports
    open_ports = ports.get("open_ports", [])

    for port in open_ports:

        if port["port"] == 22:

            if ports.get("host") == "127.0.0.1":
                issues.append(
                    "SSH running on localhost only"
                )

            else:
                score -= 10
                issues.append(
                    "SSH exposed externally"
                )

        else:
            score -= 10
            issues.append(
                f"Open port {port['port']} ({port['service']})"
            )

    # Suspicious processes
    suspicious = processes.get("suspicious", [])

    if suspicious:
        score -= 30
        issues.append("Suspicious processes detected")

    # Do not allow less than 0
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
        "issues": issues
    }
