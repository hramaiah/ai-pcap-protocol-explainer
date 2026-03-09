"""
flow_builder.py

Purpose:
Convert packet data into readable communication flows.

Example output:
Client → Switch : DHCP Discover
Server → Client : HTTP
"""

from role_detector import detect_role
from protocol_detector import detect_protocol


def build_flow(packets):

    flows = []

    for packet in packets:

        src_ip = packet["src_ip"]
        dst_ip = packet["dst_ip"]

        src_role = detect_role(src_ip)
        dst_role = detect_role(dst_ip)

        protocol = detect_protocol(packet)

        # -------------------
        # Protocol state hints
        # -------------------

        state = protocol

        # DHCP state
        if protocol == "DHCP":

            dhcp_type = packet.get("dhcp_type")

            dhcp_map = {
            "1": "DHCP Discover",
            "2": "DHCP Offer",
            "3": "DHCP Request",
            "4": "DHCP Decline",
            "5": "DHCP ACK",
            "6": "DHCP NAK",
            "7": "DHCP Release",
            "8": "DHCP Inform"
        }

            if dhcp_type in dhcp_map:
                state = dhcp_map[dhcp_type]
            else:
                state = "DHCP"

        # TCP handshake hints
        elif protocol == "TCP":

            flags = packet.get("tcp_flags")

            if flags == "0x0002":
                state = "TCP SYN"

            elif flags == "0x0012":
                state = "TCP SYN-ACK"

            elif flags == "0x0010":
                state = "TCP ACK"

        flow = f"{src_role} → {dst_role} : {state}"

        flows.append(flow)

    return flows