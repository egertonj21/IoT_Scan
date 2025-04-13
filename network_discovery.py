import nmap

def discover_active_hosts(ip_range):
    nm = nmap.PortScanner()
    print(f"Scanning network: {ip_range}")
    nm.scan(hosts=ip_range, arguments='-sn')  # Ping scan
    live_hosts = []

    for host in nm.all_hosts():
        if nm[host].state() == "up":
            live_hosts.append(host)
    return live_hosts
