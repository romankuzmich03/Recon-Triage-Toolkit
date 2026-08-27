from collectors.system import collect_system_info
from reports.writer import save_json_report

def main():

    system_info = collect_system_info()

    print("=== System Information ===")

    for key, value in system_info.items():
        print(f"{key}: {value}")

    report = save_json_report(system_info)

    print()
    print(f"Report saved: {report}")

if __name__ == "__main__":
    main()
