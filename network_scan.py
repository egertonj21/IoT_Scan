import os
import nmap

# Set the path to nmap if it's not found in the PATH
os.environ["PATH"] += r";C:\Program Files (x86)\Nmap"  # Adjust the path to your nmap location

def general_ip_scan(subnet):
    nm = nmap.PortScanner()
    try:
        # Perform a ping scan on the given subnet to discover active hosts
        nm.scan(hosts=subnet, arguments='-sn')  # -sn for ping scan (no port scan)
        active_ips = nm.all_hosts()  # Returns a list of active IPs
        return active_ips
    except nmap.nmap.PortScannerError as e:
        print(f"Error during IP scan: {e}")
        return []
