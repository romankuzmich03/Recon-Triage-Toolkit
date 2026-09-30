import platform
import os
from pathlib import Path
from datetime import datetime


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

    except (PermissionError, FileNotFoundError, OSError):

        return []



def collect_logs_info(limit=20):

    system = platform.system()

    logs = {
        "system": system,
        "collected_at": datetime.now().isoformat(),
        "sources": []
    }


    # macOS

    if system == "Darwin":

        paths = [
            "/var/log/system.log",
            "/var/log/install.log"
        ]


    # Linux

    elif system == "Linux":

        paths = [
            "/var/log/syslog",
            "/var/log/auth.log"
        ]


    # Windows

    elif system == "Windows":

        return {
            "system": "Windows",
            "sources": [
                {
                    "name": "Windows Event Logs",
                    "status": "Use Event Viewer API"
                }
            ]
        }


    else:

        paths = []


    for path in paths:

        if os.path.exists(path):

            logs["sources"].append(
                {
                    "file": path,
                    "events": read_last_lines(
                        path,
                        limit
                    )
                }
            )


    return logs