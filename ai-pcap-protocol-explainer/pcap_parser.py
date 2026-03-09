"""
pcap_parser.py

Purpose:
Parse PCAP files and extract structured packet information.

Extracts:
- IP addresses
- Ports
- Protocol
- DHCP message type
- TCP flags
"""

import pyshark


def parse_pcap(file_path):

    capture = pyshark.FileCapture(file_path)

    packets = []

    for packet in capture:

        try:

            if 'IP' not in packet:
                continue

            src_ip = packet.ip.src
            dst_ip = packet.ip.dst

            protocol = packet.highest_layer
            timestamp = packet.sniff_time

            src_port = None
            dst_port = None

            if 'TCP' in packet:
                src_port = packet.tcp.srcport
                dst_port = packet.tcp.dstport

            elif 'UDP' in packet:
                src_port = packet.udp.srcport
                dst_port = packet.udp.dstport

            # -------------------
            # Optional protocol fields
            # -------------------

            dhcp_type = None
            tcp_flags = None

            # DHCP message type
            if 'DHCP' in packet:
                try:
                    dhcp_type = packet.dhcp.option_dhcp
                except:
                    pass

            # TCP flags
            if 'TCP' in packet:
                try:
                    tcp_flags = packet.tcp.flags
                except:
                    pass

            packets.append({
                "timestamp": timestamp,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": protocol,
                "dhcp_type": dhcp_type,
                "tcp_flags": tcp_flags
            })

        except AttributeError:
            continue

    capture.close()

    return packets