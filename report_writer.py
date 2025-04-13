import json
import csv
from datetime import datetime

def write_report(scan_results, filename_prefix="iot_network_report", json_output=False, csv_output=False):
    # Generate timestamp for the filename
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if json_output:
        file_extension = '.json'
    elif csv_output:
        file_extension = '.csv'
    else:
        file_extension = '.txt'
        
    filename = f"{filename_prefix}_{timestamp}{file_extension}"

    # Summary statistics
    total_devices = len(scan_results)
    devices_with_ports = sum(1 for device in scan_results.values() if device['open_ports'])
    devices_with_filtered_ports = sum(1 for device in scan_results.values() if device['filtered_ports'])
    known_vendors = sum(1 for device in scan_results.values() if device['vendor'] != "Unknown")
    os_detected = sum(1 for device in scan_results.values() if device.get('os') not in [None, "Unknown"])

    if json_output:
        # Write the data in JSON format
        data = {
            "generated_at": now,
            "total_devices": total_devices,
            "devices_with_open_ports": devices_with_ports,
            "filtered_ports" : devices_with_filtered_ports,
            "known_vendors": known_vendors,
            "os_detected": os_detected,
            "devices": []
        }

        for ip, device in scan_results.items():
            device_info = {
                "ip_address": ip,
                "mac_address": device['mac'],
                "vendor": device['vendor'],
                "os_guess": device.get('os', 'Unknown'),
                "open_ports": [{"port": port, "state": state, "service": service} for port, state, service in device['open_ports']] if device['open_ports'] else "None",
                "filtered_ports": [{"port": port, "state": state, "service": service} for port, state, service in device['filtered_ports']] if device['filtered_ports'] else "None"
            }
            data["devices"].append(device_info)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    elif csv_output:
        # Write the data in CSV format
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['IP Address', 'MAC Address', 'Vendor', 'OS Guess', 'Open Ports', 'Filtered Ports'])

            for ip, device in scan_results.items():
                open_ports = ", ".join([f"Port {port} ({service}): {state}" for port, state, service in device['open_ports']]) if device['open_ports'] else "None"
                filtered_ports = ", ".join([f"Port {port} ({service}): {state}" for port, state, service in device['filtered_ports']]) if device['filtered_ports'] else "None"
                writer.writerow([ip, device['mac'], device['vendor'], device.get('os', 'Unknown'), open_ports, filtered_ports])

    else:
        # Write the data in text format
        with open(filename, 'w') as f:
            f.write(f"IoT Network Scan Report\nGenerated: {now}\n")
            f.write("=" * 50 + "\n\n")
            f.write("Summary:\n")
            f.write(f"  Total Devices Found: {total_devices}\n")
            f.write(f"  Devices with Open Ports: {devices_with_ports}\n")
            f.write(f"  Devices with Filtered Ports: {devices_with_filtered_ports}\n")
            f.write(f"  Devices with Known Vendor: {known_vendors}\n")
            f.write(f"  Devices with OS Detected: {os_detected}\n")
            f.write("\n" + "=" * 50 + "\n\n")

            # Write details for each device
            for ip, device in scan_results.items():
                f.write(f"IP Address: {ip}\n")
                f.write(f"MAC Address: {device['mac']}\n")
                f.write(f"Vendor: {device['vendor']}\n")
                f.write(f"OS Guess: {device.get('os', 'Unknown')}\n")
                f.write("Open Ports:\n")
                if device['open_ports']:
                    for port, state, service in device['open_ports']:
                        f.write(f"  - Port {port} ({service}): {state}\n")
                else:
                    f.write("  None found.\n")
                if device['filtered_ports']:
                    for filtered_port in device['filtered_ports']:
                        if isinstance(filtered_port, tuple) and len(filtered_port) == 2:
                            port, service = filtered_port
                            f.write(f"  - Port {port} ({service}): filtered\n")
                        else:
                            # If it's not a tuple of length 2, just print the port number
                            f.write(f"  - Port {filtered_port}: filtered\n")
                else:
                    f.write("  None found.\n")
                f.write("\n" + "-" * 40 + "\n\n")

    print(f"[+] Report written to {filename}")
