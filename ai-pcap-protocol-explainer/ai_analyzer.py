import ollama
from knowledge_retriever import retrieve_protocol_docs


def analyze_flow(session_summaries, protocols):

    protocol_docs = retrieve_protocol_docs(protocols)

    flow_text = "\n\n".join(session_summaries[:5])
    proto_text = ", ".join(sorted(protocols))

    prompt = f"""
You are a networking protocol expert.

Relevant protocol documentation:

{protocol_docs}

Protocols detected in this packet capture:
{proto_text}

Observed network sessions:
{flow_text}

Tasks:
1. Explain what protocol interactions occurred
2. Identify if the sequence is normal according to the RFC
3. Highlight possible issues
4. Suggest debugging steps
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]