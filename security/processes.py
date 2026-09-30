import psutil
import time
import hashlib
from security.process_reputation import analyse_process_reputation

def calculate_file_hash(file_path):

    if not file_path or file_path == "Unknown":
        return "Unknown"

    try:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, FileNotFoundError, OSError):
        return "Unknown"

def collect_process_info(limit=10):

    processes = []

    # First CPU measurement
    for process in psutil.process_iter():
        try:
            process.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):

            pass

    time.sleep(1)

    # Second CPU measurement
    for process in psutil.process_iter(
            [
                "pid",
                "ppid",
                "name",
                "memory_percent",
                "exe",
                "cmdline",
                "username"
            ]
    ):

        try:
            info = process.info

            exe_path = info["exe"] or "Unknown"

            cpu_count = psutil.cpu_count(logical=True) or 1

            process_data = {
                "pid": info["pid"],
                "ppid": info["ppid"],
                "name": info["name"],
                "exe": exe_path,
                "user": info["username"],
                "hash": calculate_file_hash(exe_path),
                "cmdline": info["cmdline"] or [],
                "cpu": round(process.cpu_percent() / cpu_count, 2),
                "memory": info["memory_percent"]
            }

            process_data["reputation"] = analyse_process_reputation(
                process_data
            )

            processes.append(process_data)


        except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):

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
