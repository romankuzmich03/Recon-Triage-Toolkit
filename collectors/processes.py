import psutil
import time


def collect_process_info(limit=10):

    processes = []

    # First CPU measurement
    for process in psutil.process_iter():
        try:
            process.cpu_percent()
        except Exception:
            pass

    time.sleep(1)

    # Second CPU measurement
    for process in psutil.process_iter(
        ["pid", "name", "memory_percent"]
    ):
        try:
            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu": process.cpu_percent(),
                "memory": info["memory_percent"]
            })

        except Exception:
            pass

    processes = sorted(
        processes,
        key=lambda x: x["cpu"] or 0,
        reverse=True
    )

    return {
        "top_processes": processes[:limit],
        "suspicious": [],
        "status": "OK"
    }
