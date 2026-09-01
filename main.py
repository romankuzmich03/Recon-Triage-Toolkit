from collectors.system import collect_system_info
from reports.writer import save_json_report
from collectors.network import collect_network_info
from collectors.processes import collect_process_info
from collectors.resources import collect_resources_info
from collectors.battery import collect_battery_info
from collectors.datetime import collect_datetime_info
from collectors.health import analyze_health
from security.firewall import check_firewall
from security.ports import check_ports
from security.score import calculate_security_score
from reports.generator import save_report
from collectors.connections import collect_connections_info
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

    firewall_info = check_firewall()

    ports_info = check_ports()
    
    connections_info = collect_connections_info()

    security_score = calculate_security_score(
        firewall_info,
        ports_info,
        processes_info
    )

    report_data = {
        "system": system_info,
        "network": network_info,
        "resources": resources_info,
        "battery": battery_info,
        "health": health_info,
        "firewall": firewall_info,
        "ports": ports_info,
        "processes": processes_info,
        "security_score": security_score,
        "connections": connections_info
    }

    save_report(report_data)


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
 
        print()
        print("Firewall:")
        print(firewall_info)

        print()
        print("Ports:")
        print(ports_info)

        print()
        print("Processes:")
        print(processes_info)

        print()
        print("Security Score:")
        print(security_score)

        print()
        print("Connections:")
        print(connections_info)

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
        "health": health_info,
        "firewall": firewall_info
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
