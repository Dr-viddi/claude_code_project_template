# frontend/app.py
#
# Intention:
#   Reference UI shell. Containerized separately so the API and the frontend can
#   scale, deploy, and fail independently. Replace the stub with whichever
#   framework fits the project (Streamlit, Next.js, Gradio, plain HTML, ...).
#
# What this file should contain (Streamlit example):
#   - Read `API_URL` from env (e.g. `http://app:8000`).
#   - Maintain `messages` in session state.
#   - Render existing turns with `st.chat_message(...)`.
#   - On user submit:
#       * POST to `<API_URL>/v1/chat` with the conversation so far.
#       * Append the response to session state and render it.
#   - Surface citations and trace_id for debuggability.
#
# Example (commented):
#
#   import os, httpx, streamlit as st
#   API = os.getenv("API_URL", "http://app:8000")
#
#   st.title("<project>")
#   if "messages" not in st.session_state:
#       st.session_state.messages = []
#   for m in st.session_state.messages:
#       st.chat_message(m["role"]).write(m["content"])
#   if prompt := st.chat_input("Ask something"):
#       st.session_state.messages.append({"role": "user", "content": prompt})
#       resp = httpx.post(f"{API}/v1/chat", json={...})
#       ...
