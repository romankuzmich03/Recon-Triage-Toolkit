import subprocess


def check_firewall():
    try:
        result = subprocess.check_output(
            [
                "/usr/libexec/ApplicationFirewall/socketfilterfw",
                "--getglobalstate"
            ],
            text=True
        )

        if "enabled" in result.lower():
            return {
                "firewall": "enabled",
                "status": "OK"
            }
        return {
            "firewall": "disabled",
            "status": "WARNING"
        }
    except Exception as e:
        return {
            "firewall": "unknown",
            "error": str(e)
        }
