def analyze_health(resources, battery):
    warnings = []

    if resources["memory"]["percent"] > 80:
        warnings.append("High memory usage")

    if resources["disk"]["percent"] > 90:
        warnings.append("Low disk space")

    if battery.get("percent", 100) < 20:
        warnings.append("Low battery")

    if not warnings:
        status = "ok"
        warnings.append("System looks healthy")

    elif len(warnings) < 3:
        status = "warning"
   
    else:
        status = "critical"

    return {
        "status": status,
        "messages": warnings
    }
