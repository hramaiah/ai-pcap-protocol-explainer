"""
exos_capture.py

Purpose
-------
Automates packet capture on an ExtremeXOS switch.

Instead of manually running commands on the switch like:

    debug packet capture on file-name capture.pcap count 200
    debug packet capture off

This module will:

1. Connect to the switch using SSH
2. Remove old PCAP files (cleanup)
3. Start packet capture
4. Capture packets for a specified duration
5. Stop the capture
6. Download the PCAP file locally

The downloaded PCAP will then be analyzed by the AI PCAP Protocol Explainer pipeline.

Important Note
--------------
ExtremeXOS does NOT support capture duration directly.
It supports:

    debug packet capture ... count <number_of_packets>

So we implement duration by:

    start capture
    wait N seconds
    stop capture
"""

import paramiko
import time
from scp import SCPClient


def connect_switch(host, username, password):
    """
    Establish SSH connection to the EXOS switch.
    """

    ssh = paramiko.SSHClient()

    # Automatically trust unknown SSH keys
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"\nConnecting to switch {host}...")

    ssh.connect(hostname=host, username=username, password=password)

    print("SSH connection established.\n")

    return ssh


def cleanup_old_pcaps(ssh):
    """
    Remove old PCAP files from the switch.

    EXOS stores packet captures in:
        /usr/local/tmp/

    Cleaning prevents storage buildup on the switch.
    """

    print("Cleaning old PCAP files from switch...")

    ssh.exec_command("rm -f /usr/local/tmp/*.pcap")

    print("Old PCAP files removed.\n")


def start_capture(ssh, ports=None, interface=None, filename="exos_capture.pcap", count=200):
    """
    Start packet capture on the EXOS switch.

    Parameters
    ----------
    ssh : active SSH session
    ports : capture specific switch ports (example "1:1")
    interface : capture specific interface
    filename : name of PCAP file created on switch
    count : safety packet limit
    """

    print("Starting packet capture on switch...")

    # Build EXOS capture command
    if ports:
        command = f"debug packet capture ports {ports} on file-name {filename} count {count}"

    elif interface:
        command = f"debug packet capture on interface {interface} file-name {filename} count {count}"

    else:
        command = f"debug packet capture on file-name {filename} count {count}"

    print("Executing command:")
    print(command)

    ssh.exec_command(command)

    print("Packet capture started.\n")


def stop_capture(ssh):
    """
    Stop packet capture on the switch.
    """

    print("Stopping packet capture...")

    ssh.exec_command("debug packet capture off")

    print("Capture stopped.\n")


def download_pcap(ssh, filename):
    """
    Download PCAP file from the switch.

    EXOS saves capture files under:
        /usr/local/tmp/

    Returns
    -------
    local_file : local path to downloaded PCAP
    """

    remote_file = f"/usr/local/tmp/{filename}"
    local_file = f"test_pcaps/{filename}"

    print("Downloading PCAP file from switch...")

    scp = SCPClient(ssh.get_transport())

    scp.get(remote_file, local_file)

    scp.close()

    print("PCAP downloaded successfully.")
    print(f"Local file location: {local_file}\n")

    return local_file


def capture_pcap(host, username, password, duration=10, ports=None, interface=None):
    """
    High-level function controlling the full capture workflow.

    Steps
    -----
    1. Connect to switch
    2. Clean old PCAP files
    3. Start packet capture
    4. Wait for specified duration
    5. Stop capture
    6. Download PCAP

    Parameters
    ----------
    host : switch IP
    username : SSH username
    password : SSH password
    duration : capture duration in seconds
    ports : optional port list
    interface : optional interface

    Returns
    -------
    local_file : downloaded PCAP file path
    """

    filename = "exos_capture.pcap"

    # Step 1 — connect to switch
    ssh = connect_switch(host, username, password)

    # Step 2 — cleanup old capture files
    cleanup_old_pcaps(ssh)

    # Step 3 — start capture
    start_capture(
        ssh,
        ports=ports,
        interface=interface,
        filename=filename
    )

    print(f"Capturing packets for {duration} seconds...\n")

    # Step 4 — wait during capture
    time.sleep(duration)

    # Step 5 — stop capture
    stop_capture(ssh)

    # Give switch time to finalize file
    time.sleep(2)

    # Step 6 — download PCAP
    local_file = download_pcap(ssh, filename)

    # Close SSH connection
    ssh.close()

    print("Capture session complete.\n")

    return local_file