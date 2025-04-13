import nmap
from manuf import manuf

def scan_ports(ip, ports, detect_os=True):  # Add detect_os argument
    nm = nmap.PortScanner()
    result = {
        "ip": ip,
        "open_ports": [],
        "filtered_ports": [],  # List to hold filtered ports
        "mac": None,
        "vendor": "Unknown",  # Default vendor if we can't determine it
        "os": "Unknown"
    }

    try:
        nm.scan(hosts=ip, arguments=f'-O -p {ports}')
        if ip in nm.all_hosts():
            # Extract open ports and their states
            if 'tcp' in nm[ip]:
                for port in nm[ip]['tcp']:
                    port_state = nm[ip]['tcp'][port]['state']
                    service_name = nm[ip]['tcp'][port].get('name', 'Unknown Service')
                    
                    if port_state == 'open':
                        result["open_ports"].append((port, port_state, service_name))
                    elif port_state == 'filtered':
                        result["filtered_ports"].append((port, port_state, service_name))

            # Extract MAC address and use manuf to get vendor
            if 'addresses' in nm[ip] and 'mac' in nm[ip]['addresses']:
                result["mac"] = nm[ip]['addresses']['mac']
                mac_parser = manuf.MacParser()
                vendor = mac_parser.get_manuf(result["mac"])  # Get the manufacturer
                if vendor:
                    result["vendor"] = vendor
            
            # Extract OS information only if detect_os is True
            if detect_os and 'osmatch' in nm[ip]:
                os_matches = nm[ip]['osmatch']
                if os_matches:
                    result["os"] = os_matches[0]['name']
    except Exception as e:
        print(f"Error scanning {ip}: {e}")

    return result
