import psutil


def collect_battery_info():
    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "battery": "Not available"
        }

    seconds_left = battery.secsleft

    if seconds_left is not None and int(seconds_left) < 0:
        seconds_left = None

    return {
        "percent": battery.percent,
        "charging": battery.power_plugged,
        "seconds_left": seconds_left
    }
