import psutil
import time


SUSPICIOUS_NAMES = [
    "miner",
    "keylogger",
    "backdoor",
    "malware",
    "rat"
]

SAFE_PROCESSES = [
    "kernel_task",
    "launchd",
    "logd",
    "UserEventAgent",
    "fseventsd",
    "systemstats",
    "DiskArbitration",
    "Safari",
    "Finder"
    "generativeexperiencesd",
    "MigrationSubscri",
    "systemmigrationd",
    "SAExtensionOrchestrator",
    "ASConfigurationSubscriber",
    "CloudPhotosConfiguration",
    "generativeexperiencesd",
]

def analyse_processes(limit=10):
    processes = []
    suspicious = [] 

    for proc in psutil.process_iter():
        try:
            proc.cpu_percent()
        except:
            pass

    time.sleep(1)


    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent", "username"]
    ):
        try:
            info = proc.info

            name = info["name"] or ""
       
            process_data = {
                 "pid": info["pid"],
                 "name": name,
                 "cpu": info["cpu_percent"],
                 "user": info["username"]
            }

            processes.append(process_data)

            name_lower = name.lower()

            if any(safe.lower() in name_lower for safe in SAFE_PROCESSES):
                continue

            for bad in SUSPICIOUS_NAMES:
                if bad in name_lower:
                    suspicious.append(process_data)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            continue


    process = sorted(
        processes,
        key=lambda x: x["cpu"] or 0,
        reverse=True
    )

    
    return {
        "top_processes": processes[:limit],
        "suspicious": suspicious,
        "status": "WARNING" if suspicious else "OK"
    }
