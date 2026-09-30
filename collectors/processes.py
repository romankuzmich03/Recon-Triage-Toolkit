import psutil
import hashlib


def calculate_file_hash(file_path):

    if not file_path:
        return "Unknown"

    try:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (
        PermissionError,
        FileNotFoundError,
        OSError
    ):
        return "Unknown"



def collect_process_info(limit=10):

    processes = []


    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "exe",
            "username",
            "memory_percent",
            "cmdline"
        ]
    ):

        try:

            info = process.info

            exe = info.get("exe") or "Unknown"


            processes.append(
                {
                    "pid": info.get("pid"),
                    "name": info.get("name"),
                    "exe": exe,
                    "user": info.get("username"),
                    "memory": info.get(
                        "memory_percent",
                        0
                    ),
                    "cmdline": info.get(
                        "cmdline",
                        []
                    ),
                    "hash": calculate_file_hash(exe),
                    "cpu": process.cpu_percent()
                }
            )


        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            continue


    processes = sorted(
        processes,
        key=lambda x: x["cpu"],
        reverse=True
    )


    return {
        "top_processes": processes[:limit],
        "status": "OK"
    }