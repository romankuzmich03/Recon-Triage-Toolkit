from datetime import datetime
import time


def collect_datetime_info():
    return {
        "current_time": datetime.now().isoformat(),
        "timestamp": int(time.time())
    }
