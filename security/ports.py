import socket



COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3389: "PDP"
}

def check_ports(host="127.0.0.1"):
    open_ports = []
    
    for port, name in COMMON_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
    
        result = sock.connect_ex((host, port))
 
        if result == 0:
           open_ports.append({
               "port": port,
               "service": name,
               "status": "OPEN"
           })

        sock.close()
    return{
        "host": host,
        "open_ports": open_ports,
        "status": "OK" if not open_ports else "WARNING"
    }
