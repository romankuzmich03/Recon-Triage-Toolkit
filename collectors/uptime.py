import psutil
from datetime import datetime


def collect_uptime_info():
    boot_time = psutil.boot_time()
    uptime_seconds = datetime.now().timestamp() - boot_time

    return {
        "boot_time": datetime.fromtimestamp(boot_time).isoformat(),
        "uptime_seconds": int(uptime_seconds)
    }
