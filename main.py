from collectors.system import collect_system_info
from reports.writer import save_json_report
from collectors.network import collect_network_info
from collectors.processes import collect_process_info
from collectors.resources import collect_resources_info
from collectors.battery import collect_battery_info
from collectors.datetime import collect_datetime_info
from collectors.health import analyze_health
import argparse
import sys
from colorama import Fore, Style, init

init()

def main(args):

    system_info = collect_system_info()

    network_info = collect_network_info()

    resources_info = collect_resources_info()

    processes_info = collect_process_info()
    
    battery_info = collect_battery_info()

    datetime_info = collect_datetime_info()

    health_info = analyze_health(resources_info, battery_info)

    if args.full:
        print("==== Full System Information ====")
        print()

        print("System:")
        print(system_info)

        print()
        print("Network:")
        print(network_info)

        print()
        print("Resources:")
        print(resources_info)

        print()
        print("Battery:")
        print(battery_info)

        print()
        print("Health:")
        print(health_info)
 
        return

    if args.summary:
        print("=== System Health Summary ===")
        print()

        print("Status:")
        
        if health_info["status"] == "ok":
            print(Fore.GREEN + "OK" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + health_info["status"].upper() + Style.RESET_ALL)

        print()

        print("Messages:")
        for message in health_info["messages"]:
            print("-", message)

    return

    print("=== System Information ===")

    for key, value in system_info.items():
        print(f"{key}: {value}")

    full_report = {
        "system": system_info,
        "network": network_info,
        "processes": processes_info,
        "resources": resources_info,
        "battery": battery_info,
        "datetime": datetime_info,
        "health": health_info
    }

    report = save_json_report(full_report)

    print()
    print(f"Report saved: {report}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cross Platform Triage Tool"
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show system health summary"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Show full system information"
    )

    args = parser.parse_args()

    main(args)
