FAILED_PATTERNS = [
    "failed login",
    "authentication failure",
    "invalid user",
    "failed password",
    "incorrect password"
]


def analyse_logs(logs):

    findings = []

    sources = logs.get(
        "sources",
        []
    )

    for source in sources:

        events = source.get(
            "events",
            []
        )

        for event in events:

            event_lower = event.lower()

            for pattern in FAILED_PATTERNS:

                if pattern in event_lower:

                    findings.append(
                        {
                            "file": source.get("file"),
                            "event": event,
                            "risk": "MEDIUM"
                        }
                    )

    return {
        "failed_attempts": findings,
        "count": len(findings),
        "status": (
            "WARNING"
            if findings
            else "OK"
        )
    }