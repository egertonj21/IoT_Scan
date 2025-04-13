from network_discovery import discover_active_hosts
from port_scan import scan_ports
from report_writer import write_report

# Define your subnet and ports to scan
subnet = "192.168.0.0/24"
ports_to_scan = "22,80,443,1883,21,23,25,110,143,3389,3306,5432"   # comma-separated string of ports to scan

def main():
    active_hosts = discover_active_hosts(subnet)
    results = {}

    for ip in active_hosts:
        print(f"Scanning {ip}...")
        scan_result = scan_ports(ip, ports_to_scan)
        if scan_result:
            results[ip] = scan_result

    write_report(results)

if __name__ == "__main__":
    main()
