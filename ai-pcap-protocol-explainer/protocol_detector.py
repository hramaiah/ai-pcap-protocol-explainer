def detect_protocol(packet):

    sport = packet["src_port"]
    dport = packet["dst_port"]
    proto = packet["protocol"]

    # DNS
    if sport == "53" or dport == "53":
        return "DNS"

    # DHCP
    if sport in ["67", "68"] or dport in ["67", "68"]:
        return "DHCP"

    # HTTP
    if sport == "80" or dport == "80":
        return "HTTP"

    # HTTPS / TLS
    if sport == "443" or dport == "443":
        return "TLS"

    # SSH
    if sport == "22" or dport == "22":
        return "SSH"

    # RADIUS
    if sport in ["1812", "1813"] or dport in ["1812", "1813"]:
        return "RADIUS"

    return proto