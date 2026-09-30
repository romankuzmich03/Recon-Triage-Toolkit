from collectors.system import collect_system_info
from collectors.network import collect_network_info
from collectors.processes import collect_process_info
from collectors.resources import collect_resources_info
from collectors.battery import collect_battery_info
from collectors.datetime_info import collect_datetime_info
from collectors.health import analyze_health

from security.firewall import check_firewall
from security.ports import check_ports
from security.score import calculate_security_score
from analysers.log_analyser import analyse_logs
from analysers.process_analyzer import analyse_processes

from collectors.connections import collect_connections_info
from collectors.logs import collect_logs_info

from reports.generator import save_report
from reports.html_report import save_html_report

import argparse

from colorama import Fore, Style, init


init()

def main(arguments):

    print("""
    ==============================
     Cross-Platform Triage Tool
     SOC Security Dashboard
    ==============================

    1. Scan local machine
    2. Remote scan

    """)

    choice = input("Select option: ")

    if choice == "2":

        print(
            "\nRemote scanning is not implemented yet."
        )

        print(
            "Use local scan on the target machine."
        )

        return


    elif choice != "1":

        print(
            "Invalid option"
        )

        return

    # System information
    system_info = collect_system_info()

    # Network information
    network_info = collect_network_info()

    # Resources
    resources_info = collect_resources_info()

    # Processes
    processes_info = collect_process_info()

    process_analysis = analyse_processes(
        processes_info["top_processes"]
    )

    # Battery
    battery_info = collect_battery_info()

    # Date and time
    datetime_info = collect_datetime_info()

    # Health
    health_info = analyze_health(
        resources_info,
        battery_info
    )

    # Firewall
    firewall_info = check_firewall()

    # Ports
    ports_info = check_ports()

    # Network connections
    connections_info = collect_connections_info()

    # Logs
    logs_info = collect_logs_info()

    log_analysis = analyse_logs(
        logs_info
    )

    # Security score
    security_score = calculate_security_score(
        firewall_info,
        ports_info,
        process_analysis,
        connections_info,
        log_analysis
    )
    # Report
    report_data = {
        "system": system_info,
        "network": network_info,
        "resources": resources_info,
        "battery": battery_info,
        "datetime": datetime_info,
        "health": health_info,
        "firewall": firewall_info,
        "ports": ports_info,
        "processes": processes_info,
        "process_analysis": process_analysis,
        "security_score": security_score,
        "connections": connections_info,
        "logs": logs_info,
        "log_analysis": log_analysis
    }

    save_report(report_data)
    html_report = save_html_report(
        report_data
    )

    print(
        f"HTML report saved: {html_report}"
    )

    # Full output
    if arguments.full:

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
        print("Date and Time:")
        print(datetime_info)

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
        print("Process Analysis:")
        print(process_analysis)

        print()
        print("Security Score:")
        print(security_score)

        print()
        print("Connections:")
        print(connections_info)

        print()
        print("Logs:")
        print(logs_info)

        print()
        print("Log Analysis:")
        print(log_analysis)

        return

    # Summary output
    if arguments.summary:

        print("=== System Health Summary ===")
        print()

        print("Status:")

        if health_info["status"] == "ok":
            print(
                Fore.GREEN
                + "OK"
                + Style.RESET_ALL
            )
        else:
            print(
                Fore.YELLOW
                + health_info["status"].upper()
                + Style.RESET_ALL
            )

        print()

        print("Messages:")

        for message in health_info["messages"]:
            print("-", message)

        print()

        print("Security Score:")

        print(
            security_score["score"],
            "-",
            security_score["status"]
        )

    return


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