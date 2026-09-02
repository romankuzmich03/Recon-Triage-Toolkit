import json
from datetime import datetime


def save_report(data, filename="reports/report.json"):

    report = {
        "generated": datetime.now().isoformat(),
 
        "summary": {
            "security_status": data.get("security_score", {}).get("status"),
            "security_score": data.get("security_score", {}).get("score"),
            "issues_found": len(
                data.get("security_score", {}).get("issues", [])
            ),
            "connections_checked": data.get("connections", {}).get("count", 0)
        },

        "data": data
    }

    with open(filename, "w") as file:
        json.dump(
            report,
            file,
            indent=4
        )

    return filename

