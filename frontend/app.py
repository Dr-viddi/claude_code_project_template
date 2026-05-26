"""Minimal Streamlit chat UI. Containerized separately from the API."""

from __future__ import annotations

import os

import httpx
import streamlit as st

API = os.getenv("API_URL", "http://app:8000")

st.title("Claude Code Template")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with httpx.Client(timeout=30) as client:
        resp = client.post(f"{API}/v1/chat", json={"messages": st.session_state.messages})
    answer = resp.json().get("answer", "(no answer)")
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
