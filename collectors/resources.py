import psutil


def collect_resources_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    resources = {
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    }

    return resources
