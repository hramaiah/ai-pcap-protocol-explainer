"""
knowledge_retriever.py

Purpose:
Retrieve RFC documentation references for detected protocols.

This module reads the RFC mapping file located in:
knowledge_base/rfc_index.json

It returns protocol summaries and RFC links that will be
included in the AI prompt so the LLM can reason using
authoritative networking documentation.
"""

import json
import os


def retrieve_protocol_docs(protocols):

    docs = []

    # Path to the RFC knowledge file
    kb_path = os.path.join("knowledge_base", "rfc_index.json")

    # If knowledge base file does not exist
    if not os.path.exists(kb_path):
        return ""

    # Load the RFC knowledge base
    with open(kb_path, "r") as f:
        kb = json.load(f)

    # Iterate through detected protocols
    for proto in protocols:

        if proto in kb:

            rfc = kb[proto].get("rfc", "")
            link = kb[proto].get("link", "")
            summary = kb[proto].get("summary", "")

            doc = (
                f"{proto} ({rfc})\n"
                f"{summary}\n"
                f"Reference: {link}\n"
            )

            docs.append(doc)

    return "\n".join(docs)