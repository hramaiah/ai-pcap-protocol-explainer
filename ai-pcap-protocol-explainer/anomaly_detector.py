"""
anomaly_detector.py

Purpose:
Detect common protocol anomalies before sending data to AI.
"""

def detect_anomalies(flows):

    anomalies = []

    flow_text = "\n".join(flows)

    # -------------------
    # TCP handshake check
    # -------------------

    if "TCP SYN" in flow_text and "TCP SYN-ACK" not in flow_text:
        anomalies.append("TCP SYN seen but no SYN-ACK response (possible connectivity issue)")

    # -------------------
    # DHCP negotiation check
    # -------------------

    if "DHCP Discover" in flow_text and "DHCP Offer" not in flow_text:
        anomalies.append("DHCP Discover seen but no DHCP Offer (DHCP server may be unreachable)")

    if "DHCP Offer" in flow_text and "DHCP Request" not in flow_text:
        anomalies.append("DHCP Offer seen but no DHCP Request (client did not request lease)")

    # -------------------
    # DNS response check
    # -------------------

    if "DNS" in flow_text and "Response" not in flow_text:
        anomalies.append("DNS query seen but no response (possible DNS issue)")

    return anomalies