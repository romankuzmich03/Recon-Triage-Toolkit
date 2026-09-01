import json
from datetime import datetime


def save_report(data, filename="reports/report.json"):

    report = {
        "generated": datetime.now().isoformat(),
        "data": data
    }

    with open(filename, "w") as file:
        json.dump(
            report,
            file,
            indent=4
        )

    return filename

