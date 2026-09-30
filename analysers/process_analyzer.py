SUSPICIOUS_NAMES = [
    "miner",
    "keylogger",
    "backdoor",
    "malware",
    "rat",
    "rootkit"
]


SUSPICIOUS_PATHS = [
    "/tmp",
    "/var/tmp",
    "/private/tmp",
    "/downloads"
]


def analyse_processes(processes):

    suspicious = []


    for process in processes:

        name = (
            process.get("name")
            or ""
        )

        exe = (
            process.get("exe")
            or ""
        )


        reasons = []


        name_lower = name.lower()
        exe_lower = exe.lower()


        # Process name check

        for bad in SUSPICIOUS_NAMES:

            if bad in name_lower:

                reasons.append(
                    f"Suspicious process name: {bad}"
                )


        # Executable path check

        for path in SUSPICIOUS_PATHS:

            if path in exe_lower:

                reasons.append(
                    f"Executable from suspicious path: {path}"
                )


        # CPU usage check

        cpu = process.get(
            "cpu",
            0
        )

        if cpu > 80:

            reasons.append(
                "High CPU usage"
            )


        if reasons:

            suspicious.append(
                {
                    "pid": process.get("pid"),
                    "name": name,
                    "exe": exe,
                    "reason": reasons,
                    "risk": "HIGH"
                }
            )


    return {

        "suspicious": suspicious,

        "finding_count": len(suspicious),

        "status":
            "WARNING"
            if suspicious
            else "OK"

    }