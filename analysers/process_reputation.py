import platform


MACOS_TRUSTED_PATHS = [
    "/System/",
    "/usr/libexec/",
    "/usr/sbin/",
    "/usr/bin/",
    "/bin/",
    "/sbin/"
]


LINUX_TRUSTED_PATHS = [
    "/bin/",
    "/sbin/",
    "/usr/bin/",
    "/usr/sbin/",
    "/lib/",
    "/lib64/"
]


WINDOWS_TRUSTED_PATHS = [
    "C:\\Windows\\System32\\",
    "C:\\Windows\\",
    "C:\\Program Files\\",
    "C:\\Program Files (x86)\\"
]


SUSPICIOUS_PATHS = [
    "/Downloads/",
    "/Desktop/",
    "/Temp/",
    "\\Downloads\\",
    "\\Desktop\\",
    "\\Temp\\"
]

APPLICATION_PATHS = [
    "/Applications/",
    "/Volumes/",
    "/opt/",
    "/usr/local/",
    "C:\\Program Files\\",
    "C:\\Program Files (x86)\\"
]

LOCAL_TOOL_INDICATORS = [
    "main.py",
    "cross-platform-triage-tool",
]

def get_trusted_paths():

    system = platform.system()


    if system == "Darwin":
        return MACOS_TRUSTED_PATHS


    elif system == "Linux":
        return LINUX_TRUSTED_PATHS


    elif system == "Windows":
        return WINDOWS_TRUSTED_PATHS


    return []



def analyse_process_reputation(process):

    exe = process.get("exe", "")

    result = {
        "name": process.get("name"),
        "trust": "UNKNOWN",
        "risk": "UNKNOWN",
        "reason": ""
    }

    if not exe or exe == "Unknown":

        result["reason"] = "Executable path unavailable"

        return result

    # Check suspicious locations first

    for path in SUSPICIOUS_PATHS:

        if path.lower() in exe.lower():

            result["trust"] = "SUSPICIOUS"
            result["risk"] = "HIGH"
            result["reason"] = "Executable from risky location"

            return result

    cmdline = str(process.get("cmdline", ""))

    for item in LOCAL_TOOL_INDICATORS:

        if (
                item.lower() in cmdline.lower()
                or
                item.lower() in exe.lower()
        ):
            result["trust"] = "LOCAL_TOOL"
            result["risk"] = "LOW"
            result["reason"] = "Current security tool"

            return result

    # Check system locations

    trusted_paths = get_trusted_paths()


    for path in trusted_paths:

        if exe.lower().startswith(path.lower()):
            result["trust"] = "TRUSTED"
            result["risk"] = "LOW"
            result["reason"] = "System location"

            return result



    # User applications

    for path in APPLICATION_PATHS:

        if path.lower() in exe.lower():
            result["trust"] = "APPLICATION"
            result["risk"] = "LOW"
            result["reason"] = "Installed application"

            return result

    # User directory

    exe_lower = exe.lower()

    if (
            "/users/" in exe_lower
            or
            "/home/" in exe_lower
            or
            "\\users\\" in exe_lower
    ):
        result["trust"] = "USER_PROCESS"
        result["risk"] = "MEDIUM"
        result["reason"] = "Executable from user directory"

        return result



    return result