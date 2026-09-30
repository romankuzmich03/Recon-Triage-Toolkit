import subprocess
SAFE_NETWORK_PROCESSES = [
    "ControlCenter",
    "ControlCe",
    "rapportd",
    "sharingd",
    "identityservicesd",
    "identitys",
    "replicator",
]

def collect_connections_info():
    connections = []
    seen_connections = set()

    listen_count = 0
    listening_count = 0
    established_count = 0
    local_count = 0
    private_count = 0
    external_count = 0

    try:
        result = subprocess.run(
            ["lsof", "-i", "-P", "-n"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.splitlines()

        for line in lines[1:]:
            parts = line.split()

            if len(parts) < 9:
                continue

            process = parts[0]
            pid = parts[1]
            connection = " ".join(parts[8:])

            status = "UNKNOWN"

            if "ESTABLISHED" in connection:
                status = "ESTABLISHED"
                established_count += 1
            elif "LISTEN" in connection:
                status = "LISTEN"
                listen_count += 1

            risk = "LOW"

            if "LISTEN" in status and connection.startswith("*:"):

                if process in SAFE_NETWORK_PROCESSES:
                    risk = "INFO"

                else:
                    risk = "MEDIUM"

            if (
                    "127.0.0.1" in connection
                    or "[::1]" in connection
                    or "localhost" in connection
            ):
                risk = "LOW"

            if "ESTABLISHED" in status and not (
                "127.0.0.1" in connection
                or "localhost" in connection
                or "fe80" in connection
                or "192.168." in connection
                or "10." in connection
            ):
                risk = "HIGH"

            connection_key = (
                process,
                pid,
                connection,
                status
            )

            if connection_key in seen_connections:
                continue

            seen_connections.add(connection_key)

            if (
                    "127.0.0.1" in connection
                    or "localhost" in connection
                    or "[::1]" in connection
            ):
                local_count += 1

            elif (
                    "192.168." in connection
                    or "10." in connection
                    or "172.16." in connection
            ):
                private_count += 1

            elif connection.startswith("*:"):
                listening_count += 1

            else:
                external_count += 1

            connections.append(
                {
                    "process": process,
                    "pid": pid,
                    "details": connection,
                    "status": status,
                    "risk": risk
                }
            )

    except Exception as error:
        return {
            "connections": [],
            "count": 0,
            "error": str(error)
        }

    findings = []

    for conn in connections:
        if conn["risk"] == "MEDIUM":
            findings.append(
                {
                    "level": "MEDIUM",
                    "process": conn["process"],
                    "pid": conn["pid"],
                    "message": f"Service listening: {conn['details']}",
                    "recommendation": "Check if this service should be exposed"
                }
            )

        if conn["risk"] == "HIGH":
            findings.append(
                {
                    "level": "HIGH",
                    "process": conn["process"],
                    "pid": conn["pid"],
                    "message": f"External connection: {conn['details']}",
                    "recommendation": "Investigate remote connection"
                }
            )

    return {
        "connections": connections,
        "count": len(connections),
        "listen": listen_count,
        "listening": listening_count,
        "established": established_count,
        "local": local_count,
        "private": private_count,
        "external": external_count,
        "findings": findings,
        "finding_count": len(findings)
    }
