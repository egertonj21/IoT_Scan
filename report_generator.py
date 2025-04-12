import ipaddress
from port_scan import scan_ports
from network_scan import general_ip_scan

def find_ip_range(active_ips):
    # Convert the active IPs to a list of ipaddress objects for easy comparison
    ip_objects = [ipaddress.ip_address(ip) for ip in active_ips]
    
    if not ip_objects:
        return None, None
    
    # Find the lowest and highest IPs
    lowest_ip = min(ip_objects)
    highest_ip = max(ip_objects)
    
    return str(lowest_ip), str(highest_ip)

def generate_report(subnet, ports_to_scan):
    active_ips = general_ip_scan(subnet)
    if not active_ips:
        print("No active IPs found on the network.")
        return

    # Find the lowest and highest IP in the list
    lowest_ip, highest_ip = find_ip_range(active_ips)
    
    if not lowest_ip or not highest_ip:
        print("No valid IPs found to scan.")
        return
    
    print(f"Scanning IP range from {lowest_ip} to {highest_ip}")
    
    # Scan each IP address in the range from lowest to highest
    for ip in range(int(ipaddress.ip_address(lowest_ip)), int(ipaddress.ip_address(highest_ip)) + 1):
        ip_str = str(ipaddress.ip_address(ip))
        print(f"Scanning {ip_str}...")
        open_ports = scan_ports(ip_str, ports_to_scan)
        
        if open_ports:
            print(f"Open ports on {ip_str}: {open_ports}")
        else:
            print(f"No open ports found on {ip_str}.")
