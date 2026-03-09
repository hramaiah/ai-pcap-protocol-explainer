"""
main.py

Main orchestrator for the AI PCAP Protocol Explainer.

Pipeline:

1. Capture PCAP from EXOS switch (optional)
2. Parse PCAP
3. Detect protocols
4. Build packet flows
5. Group packets into sessions
6. Detect anomalies
7. Detect protocol sequences
8. Send sessions to AI analyzer
9. Print explanation
"""

import argparse

# Parser
from pcap_parser import parse_pcap

# Flow builder
from flow_builder import build_flow

# Protocol detection
from protocol_detector import detect_protocol

# Session builder
from session_builder import build_sessions

# AI analyzer
from ai_analyzer import analyze_flow

# Anomaly detection
from anomaly_detector import detect_anomalies

# Sequence detector
from sequence_detector import detect_sequences

# EXOS packet capture
from exos_capture import capture_pcap


def main():

    # ---------------------------
    # 1️⃣ CLI ARGUMENT PARSER
    # ---------------------------
    # Allows users to either:
    #   • analyze an existing PCAP
    #   • capture packets directly from a switch

    parser = argparse.ArgumentParser(
        description="AI PCAP Protocol Explainer"
    )

    parser.add_argument(
        "--pcap",
        help="Path to PCAP file for analysis"
    )

    parser.add_argument(
        "--capture",
        action="store_true",
        help="Capture packets from EXOS switch"
    )

    parser.add_argument(
        "--switch",
        help="Switch IP address"
    )

    parser.add_argument(
        "--user",
        help="SSH username"
    )

    parser.add_argument(
        "--password",
        help="SSH password"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Packet capture duration in seconds (default: 10)"
    )

    args = parser.parse_args()

    # ---------------------------
    # 2️⃣ CAPTURE OR LOAD PCAP
    # ---------------------------

    if args.capture:

        # Validate required arguments
        if not args.switch or not args.user or not args.password:

            print("Error: --switch, --user and --password required for capture")
            return

        print("\nStarting live packet capture from EXOS switch...\n")

        pcap_file = capture_pcap(
            host=args.switch,
            username=args.user,
            password=args.password,
            duration=args.duration
        )

    elif args.pcap:

        pcap_file = args.pcap

    else:

        print("Usage:")
        print("Analyze PCAP: python main.py --pcap file.pcap")
        print("Live capture: python main.py --capture --switch <ip> --user <user> --password <pwd> --duration 20")
        return

    print("\nAnalyzing PCAP:", pcap_file)

    # ---------------------------
    # 3️⃣ PCAP PARSER
    # ---------------------------

    packets = parse_pcap(pcap_file)

    # ---------------------------
    # 4️⃣ FLOW BUILDER
    # ---------------------------

    flows = build_flow(packets)

    print("\nPacket Flow Summary:\n")

    for flow in flows[:20]:
        print(flow)

    # ---------------------------
    # 5️⃣ PROTOCOL DETECTION
    # ---------------------------

    detected_protocols = set()

    for packet in packets:
        proto = detect_protocol(packet)
        detected_protocols.add(proto)

    print("\nDetected Protocols in Capture:\n")

    for proto in sorted(detected_protocols):
        print("-", proto)

    # ---------------------------
    # 6️⃣ SESSION BUILDER
    # ---------------------------

    sessions = build_sessions(packets)

    print("\nDetected Sessions:\n")

    session_summaries = []

    for session, pkts in sessions.items():

        summary = f"Session {session}"

        for p in pkts[:10]:
            summary += (
                f"\n  {p['src_ip']}:{p['src_port']} -> "
                f"{p['dst_ip']}:{p['dst_port']} | "
                f"{p['protocol']}"
            )

        session_summaries.append(summary)

        print(summary)
        print()

    # ---------------------------
    # 7️⃣ ANOMALY DETECTION
    # ---------------------------

    print("\nChecking for protocol anomalies...\n")

    anomalies = detect_anomalies(flows)

    if anomalies:
        print("Potential Issues Detected:\n")
        for a in anomalies:
            print("-", a)
    else:
        print("No obvious anomalies detected.")

    # ---------------------------
    # 8️⃣ SEQUENCE DETECTION
    # ---------------------------

    print("\nChecking for known protocol sequences...\n")

    sequences = detect_sequences(flows)

    if sequences:
        print("Known Sequences Detected:\n")
        for s in sequences:
            print("-", s)
    else:
        print("No known protocol sequences detected.")

    # ---------------------------
    # 9️⃣ AI ANALYSIS
    # ---------------------------

    print("\nRunning AI protocol analysis...\n")

    analysis = analyze_flow(
        session_summaries + anomalies + sequences,
        detected_protocols
    )

    print("AI Analysis:\n")
    print(analysis)


if __name__ == "__main__":
    main()