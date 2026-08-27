import platform
import socket
import getpass


def collect_system_info():

    info = {
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(), 
        "architecture": platform.machine()
    }

    return info
