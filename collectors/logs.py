import platform
import os
from datetime import datetime
from typing import Any


SUSPICIOUS_KEYWORDS = [
    "failed",
    "error",
    "warning",
    "denied",
    "unauthorized",
    "attack",
    "malware",
    "login failed"
]


def read_last_lines(file_path, limit=20):

    try:
        with open(
            file_path,
            "r",
            errors="ignore"
        ) as file:

            lines = file.readlines()

            return [
                line.strip()
                for line in lines[-limit:]
            ]

    except (
        PermissionError,
        FileNotFoundError,
        OSError
    ):

        return []


def analyse_log_events(events):

    findings = []

    for event in events:

        event_lower = event.lower()

        for keyword in SUSPICIOUS_KEYWORDS:

            if keyword in event_lower:

                findings.append(
                    {
                        "event": event,
                        "keyword": keyword,
                        "severity": (
                            "HIGH"
                            if keyword in [
                                "malware",
                                "attack"
                            ]
                            else "MEDIUM"
                        )
                    }
                )

                break

    return findings



def collect_logs_info(limit=20):

    system = platform.system()

    logs: dict[str, Any] = {

        "system": system,

        "collected_at":
            datetime.now().isoformat(),

        "sources": [],

        "findings": []

    }


    if system == "Darwin":

        paths = [

            "/var/log/system.log",

            "/var/log/install.log"

        ]


    elif system == "Linux":

        paths = [

            "/var/log/syslog",

            "/var/log/auth.log"

        ]


    elif system == "Windows":

        logs["sources"].append(
            {
                "source": "Windows Event Logs",
                "status": "Event Viewer API required",
                "events": []
            }
        )

        return logs


    else:

        paths = []


    for path in paths:

        if os.path.exists(path):

            events = read_last_lines(
                path,
                limit
            )


            logs["sources"].append(
                {
                    "file": path,
                    "events": events
                }
            )


            findings = analyse_log_events(
                events
            )


            logs["findings"].extend(
                findings
            )


    logs["status"] = (
        "WARNING"
        if logs["findings"]
        else "OK"
    )


    return logs