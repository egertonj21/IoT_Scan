import argparse
from network_discovery import discover_active_hosts
from port_scan import scan_ports
from report_writer import write_report

def main():
    parser = argparse.ArgumentParser(description="IoT Network Scanner")
    parser.add_argument("ip_range", help="IP range to scan (e.g., 192.168.0.0/24)")
    parser.add_argument("--json", action="store_true", help="Generate JSON output")
    parser.add_argument("--csv", action="store_true", help="Generate CSV output")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--os", action="store_true", help="Attempt to detect OS")
    parser.add_argument("--ports", type=str, default="1-1024", help="Comma-separated list of ports to scan (default: 1-1024)")
    args = parser.parse_args()

    # Discover active hosts
    print(f"Scanning network: {args.ip_range}")
    active_hosts = discover_active_hosts(args.ip_range)

    scan_results = {}

    # Scan each active host for open ports and details
    for ip in active_hosts:
        print(f"Scanning {ip}...")
        result = scan_ports(ip, args.ports, detect_os=args.os)  # Use the ports argument
        scan_results[ip] = result

        if args.verbose:
            print(f"Scan result for {ip}: {result}")

    # Write the report in the specified format (JSON, CSV, or TXT)
    write_report(scan_results, json_output=args.json, csv_output=args.csv)

if __name__ == "__main__":
    main()
