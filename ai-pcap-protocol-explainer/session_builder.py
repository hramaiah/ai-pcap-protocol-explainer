"""
session_builder.py

Purpose:
Groups packets into bidirectional sessions (client ↔ server conversations)

Example session:
192.168.1.10:54012 <-> 93.184.216.34:80
"""

def build_sessions(packets):

    sessions = {}

    for packet in packets:

        src = packet["src_ip"]
        dst = packet["dst_ip"]
        sport = packet["src_port"]
        dport = packet["dst_port"]

        # Normalize session key so both directions belong to same session
        key = tuple(sorted([
            f"{src}:{sport}",
            f"{dst}:{dport}"
        ]))

        if key not in sessions:
            sessions[key] = []

        sessions[key].append(packet)

    return sessions