IoT Network Scanner
This script scans a specified IP range for open ports and attempts to detect devices and their operating systems. It provides detailed reports with information about discovered devices, including IP address, MAC address, vendor, operating system, and open ports.

To run the script - python app.py [IP_RANGE] [OPTIONS]

options:
  -h, --help     show this help message and exit
  --json         Generate JSON output
  --csv          Generate CSV output
  --verbose      Enable verbose output - prints results to terminal
  --os           Attempt to detect OS
  --ports PORTS  Comma-separated list of ports to scan (default: 1-1024)

Example Commands:

python app.py 192.168.1.10 - scans a specific IP with default set of ports (1-1024)
python app.py 192.168.1.0/24 --ports 22,80,443 --os - scans an entire subnet for specific ports (22,80,443) with OS detection enabled
python app.py 192.168.1.100-200 --json/csv - scans a range of IPs and produces the output in JSON/CSV format (default is .txt)
python app.py 192.168.1.0/24 --ports 80,443 --verbose - scans a subnet, with verbose output and specific ports