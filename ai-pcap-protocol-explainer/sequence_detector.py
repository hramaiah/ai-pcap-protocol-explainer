"""
sequence_detector.py

Purpose:
Detect known protocol sequences such as:
- DHCP DORA
- TCP handshake
- DNS request/response
"""

def detect_sequences(flows):

    sequences = []

    flow_text = "\n".join(flows)

    # -------------------
    # DHCP DORA
    # -------------------

    if (
        "DHCP Discover" in flow_text and
        "DHCP Offer" in flow_text and
        "DHCP Request" in flow_text and
        "DHCP ACK" in flow_text
    ):
        sequences.append("DHCP DORA sequence detected (successful lease negotiation)")

    # -------------------
    # TCP Handshake
    # -------------------

    if (
        "TCP SYN" in flow_text and
        "TCP SYN-ACK" in flow_text and
        "TCP ACK" in flow_text
    ):
        sequences.append("TCP 3-way handshake detected")

    # -------------------
    # DNS request-response
    # -------------------

    if "DNS" in flow_text:
        sequences.append("DNS traffic detected (query-response expected)")

    return sequences