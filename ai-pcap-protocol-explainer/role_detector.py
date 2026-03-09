def detect_role(ip):

    # Broadcast
    if ip == "255.255.255.255":
        return "Broadcast"

    # Typical private client range
    if ip.startswith("192.168.") or ip.startswith("10."):

        # heuristic: gateway often switch
        if ip.endswith(".1"):
            return "Switch"

        return "Client"

    return "Server"