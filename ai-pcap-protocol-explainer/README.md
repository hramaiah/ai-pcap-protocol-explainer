# AI PCAP Protocol Explainer

## Overview

**AI PCAP Protocol Explainer** is a Python-based network debugging assistant that automates packet capture from **ExtremeXOS switches**, analyzes the resulting **PCAP files**, reconstructs protocol interactions, and generates **human-readable explanations using AI**.

Instead of manually running packet captures, exporting PCAPs, and analyzing them in Wireshark, engineers can run a single script that:

1. Captures packets directly from an EXOS switch
2. Downloads the PCAP automatically
3. Parses and reconstructs protocol flows
4. Detects anomalies and known protocol sequences
5. Uses an AI model to explain the packet behavior

This significantly reduces the **time and expertise required for packet-level troubleshooting**.

---

# Key Capabilities

### Automated Packet Capture

The tool connects to an **ExtremeXOS switch via SSH** and triggers packet capture using the EXOS command:

```
debug packet capture
```

It automatically:

* Starts packet capture
* Stops capture after a configurable duration
* Downloads the PCAP file to the local system

---

### PCAP Collection & Processing

Downloaded PCAP files are parsed using Python packet analysis libraries.

Packet metadata such as:

* Source IP
* Destination IP
* Ports
* Protocols

are extracted for further analysis.

---

### Protocol Flow Reconstruction

The tool reconstructs packet interactions into readable sequences.

Example:

```
Client → Switch : EAPOL Start
Switch → Client : Identity Request
Switch → RADIUS : Access Request
```

This allows engineers to quickly understand **protocol behavior without opening Wireshark**.

---

### Protocol-Based Packet Separation

Packets are automatically grouped by protocol:

```
DHCP
DNS
TCP
RADIUS
EAPOL
```

Each protocol can then be analyzed independently.

---

### Failure & Anomaly Detection

The system detects common network issues such as:

* DHCP negotiation failures
* Missing TCP handshake packets
* Authentication failures
* Incomplete protocol sequences

Example:

```
Potential Issue Detected:
DHCP Discover observed but no Offer received
```

---

### AI-Based Protocol Explanation

A local or hosted LLM analyzes protocol flows and generates explanations.

Example AI output:

```
The packet capture shows a DHCP discovery process initiated by the client.
The server responded with an Offer and the client successfully completed
the Request and ACK steps, indicating a successful DHCP lease assignment.
```

---

### Interactive CLI Debugging

The tool runs as a **simple Python CLI application**, allowing engineers to:

* capture packets
* analyze existing PCAP files
* inspect protocol behavior quickly

---

# Architecture

```
Switch (ExtremeXOS)
      ↓
Packet Capture (SSH automation)
      ↓
PCAP Download
      ↓
PCAP Parser
      ↓
Protocol Detection
      ↓
Protocol Packet Separation
      ↓
Flow Reconstruction
      ↓
Anomaly Detection
      ↓
Sequence Detection
      ↓
AI Protocol Explanation
```

---

# Project Structure

```
ai-pcap-protocol-explainer
│
├── main.py
├── exos_capture.py
├── pcap_parser.py
├── protocol_detector.py
├── protocol_filter.py
├── flow_builder.py
├── session_builder.py
├── anomaly_detector.py
├── sequence_detector.py
├── ai_analyzer.py
│
├── test_pcaps/
│
└── README.md
```

---

# Tech Stack

| Component         | Technology               |
| ----------------- | ------------------------ |
| Language          | Python                   |
| Packet Parsing    | PyShark / Scapy          |
| Switch Automation | Paramiko (SSH)           |
| File Transfer     | SCP                      |
| AI Reasoning      | LLM APIs or local models |
| Interface         | Python CLI               |

---

# Installation

Clone the repository:

```
git clone https://github.com/<your-username>/ai-pcap-protocol-explainer.git
cd ai-pcap-protocol-explainer
```

Install dependencies:

```
pip install -r requirements.txt
```

Example dependencies:

```
paramiko
scp
pyshark
scapy
```

---

# Usage

## Analyze Existing PCAP

```
python main.py --pcap test_pcaps/sample.pcap
```

---

## Capture Packets From EXOS Switch

```
python main.py \
--capture \
--switch <switch-ip> \
--user <username> \
--password <password> \
--duration 10
```

Example:

```
python main.py \
--capture \
--switch 10.10.10.5 \
--user admin \
--password password \
--duration 15
```

The script will:

1. SSH to the switch
2. Start packet capture
3. Wait for specified duration
4. Stop capture
5. Download PCAP
6. Analyze protocol flows

---

# Example Output

```
Detected Protocols:

- DHCP
- DNS
- TCP

Packet Flow Summary:

Client → Switch : DHCP Discover
Switch → Client : DHCP Offer
Client → Switch : DHCP Request
Switch → Client : DHCP ACK

AI Analysis:

The packet capture shows a complete DHCP lease negotiation
between the client and server. No anomalies were detected.
```

---

# Target Users

This tool is designed for:

* Network Engineers troubleshooting protocol issues
* Network QA / Test Engineers debugging packet-level failures
* SRE / DevOps teams diagnosing connectivity issues
* Technical Support teams analyzing customer packet captures
* Networking learners studying protocol interactions

---

# Future Enhancements

Planned improvements include:

* automatic switch port detection using LLDP / NetLogin
* protocol-specific capture optimization
* security vulnerability detection based on observed traffic
* automatic testcase suggestions for QA testing
* interactive AI debugging assistant

---

