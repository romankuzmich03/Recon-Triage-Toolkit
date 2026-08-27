import json
from datetime import datetime


def save_json_report(data):
    filename = f"reports/system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    return filename
