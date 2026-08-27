import psutil


def collect_battery_info():
    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "battery": "Not available"
        }

    return {
        "percent": battery.percent,
        "charging": battery.power_plugged,
        "seconds_left": battery.secsleft
    }
