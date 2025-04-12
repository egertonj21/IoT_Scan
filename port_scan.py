import os
import nmap

# Set the path to nmap if it's not found in the PATH
os.environ["PATH"] += r";C:\Program Files (x86)\Nmap"  # Adjust the path to your nmap location

def scan_ports(ip_address, ports_to_scan):
    nm = nmap.PortScanner()

    # Convert the list of ports to a comma-separated string
    ports_str = ",".join(map(str, ports_to_scan))

    try:
        # Scan the IP address on the specified ports
        nm.scan(ip_address, ports_str)
        
        # Check if the scan result contains the IP address
        if ip_address not in nm.all_hosts():
            print(f"No results for IP address: {ip_address}")
            return []

        # Get the open ports from the scan result
        open_ports = []
        for port in nm[ip_address].all_protocols():
            if port == 'tcp':  # We are interested in TCP ports only
                for p in nm[ip_address][port]:
                    if nm[ip_address][port][p]['state'] == 'open':
                        open_ports.append(p)

        return open_ports

    except nmap.nmap.PortScannerError as e:
        print(f"Error scanning {ip_address}: {e}")
        return []
