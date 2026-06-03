"""Optional Streamlit chat UI, containerized separately from the API.

Run locally:  streamlit run frontend/app.py   (needs `pip install -r frontend/requirements.txt`)
Talks to the API over HTTP, so it scales/deploys independently.
"""

from __future__ import annotations

import os

import httpx
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

st.title("Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        payload = {"messages": st.session_state.messages}
        resp = httpx.post(f"{API}/v1/chat", json=payload, timeout=30)
        answer = resp.json().get("answer", "(no answer)")
    except httpx.HTTPError as exc:
        answer = f"(request failed: {exc})"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
