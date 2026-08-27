import psutil


def collect_process_info():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            processes.append(process.info)
        except Exception:
            pass

    return processes
