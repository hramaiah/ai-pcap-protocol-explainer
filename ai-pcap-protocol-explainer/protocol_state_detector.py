"""
protocol_state_detector.py

Purpose:
Detect protocol states such as:
- DHCP Discover / Offer / Request / ACK
- TCP SYN / SYN-ACK / ACK
"""

def detect_state(packet):

    proto = packet["protocol"]

    # -------------------
    # DHCP Detection
    # -------------------

    if proto == "DHCP":

        msg_type = packet.get("dhcp_type")

        if msg_type == "discover":
            return "DHCP Discover"

        if msg_type == "offer":
            return "DHCP Offer"

        if msg_type == "request":
            return "DHCP Request"

        if msg_type == "ack":
            return "DHCP ACK"

        return "DHCP"

    # -------------------
    # TCP Handshake
    # -------------------

    if proto == "TCP":

        flags = packet.get("tcp_flags")

        if flags == "S":
            return "TCP SYN"

        if flags == "SA":
            return "TCP SYN-ACK"

        if flags == "A":
            return "TCP ACK"

        return "TCP"

    return proto