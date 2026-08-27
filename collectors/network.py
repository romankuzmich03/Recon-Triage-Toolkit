import socket


def collect_network_info():
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "Unknown"

    network_info = {
        "hostname": hostname,
        "ip_address": ip_address
    }
    
    return network_info
