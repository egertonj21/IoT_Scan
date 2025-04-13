from datetime import datetime

def write_report(scan_results, filename_prefix="iot_network_report"):
    # Generate timestamp for the filename
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_prefix}_{timestamp}.txt"

    # Summary statistics
    total_devices = len(scan_results)
    devices_with_ports = sum(1 for device in scan_results.values() if device['open_ports'])
    known_vendors = sum(1 for device in scan_results.values() if device['vendor'] != "Unknown")
    os_detected = sum(1 for device in scan_results.values() if device.get('os') not in [None, "Unknown"])

    # Write the report to a file
    with open(filename, 'w') as f:
        f.write(f"IoT Network Scan Report\nGenerated: {now}\n")
        f.write("=" * 50 + "\n\n")
        f.write("Summary:\n")
        f.write(f"  Total Devices Found: {total_devices}\n")
        f.write(f"  Devices with Open Ports: {devices_with_ports}\n")
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
            f.write("\n" + "-" * 40 + "\n\n")

    print(f"[+] Report written to {filename}")
