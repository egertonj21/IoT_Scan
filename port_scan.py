import nmap
from manuf import manuf

def scan_ports(ip, ports):
    nm = nmap.PortScanner()
    result = {
        "ip": ip,
        "open_ports": [],
        "mac": None,
        "vendor": "Unknown",  # Default vendor if we can't determine it
        "os": "Unknown"
    }

    try:
        nm.scan(hosts=ip, arguments=f'-O -p {ports}')
        if ip in nm.all_hosts():
            # Extract open ports and their states
            if 'tcp' in nm[ip]:
                result["open_ports"] = [(port, nm[ip]['tcp'][port]['state'], nm[ip]['tcp'][port].get('name', 'Unknown Service')) for port in nm[ip]['tcp']]
            
            # Extract MAC address and use manuf to get vendor
            if 'addresses' in nm[ip] and 'mac' in nm[ip]['addresses']:
                result["mac"] = nm[ip]['addresses']['mac']
                mac_parser = manuf.MacParser()
                vendor = mac_parser.get_manuf(result["mac"])  # Get the manufacturer
                if vendor:
                    result["vendor"] = vendor
            
            # Extract OS information
            if 'osmatch' in nm[ip]:
                os_matches = nm[ip]['osmatch']
                if os_matches:
                    result["os"] = os_matches[0]['name']
    except Exception as e:
        print(f"Error scanning {ip}: {e}")

    return result
