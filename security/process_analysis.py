SUSPICIOUS_NAMES = [
    "miner",
    "keylogger",
    "backdoor",
    "malware",
    "rat"
]


def analyse_processes(processes):

    suspicious = []

    for process in processes:

        name = process.get("name", "")

        name_lower = name.lower()


        for bad in SUSPICIOUS_NAMES:

            if bad in name_lower:

                suspicious.append({
                    "pid": process.get("pid"),
                    "name": name,
                    "reason": f"Suspicious process name: {bad}",
                    "risk": "HIGH"
                })


    return {
        "suspicious": suspicious,
        "finding_count": len(suspicious),
        "status": "WARNING" if suspicious else "OK"
    }