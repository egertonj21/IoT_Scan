from report_generator import generate_report

if __name__ == "__main__":
    # Define the subnet to scan (for example, 192.168.1.0/24)
    subnet = "192.168.0.0/24"
    ports_to_scan = [22, 80, 443]  # Define the ports to scan

    generate_report(subnet, ports_to_scan)
