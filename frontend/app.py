# frontend/app.py
#
# Purpose
#   Reference UI shell. Containerized separately from the API so the two can
#   scale, deploy, and fail independently. Streamlit is shown here because it's
#   the fastest path from API to demo; pick whatever fits (Next.js, Gradio,
#   plain HTML).
#
# When you want a file like this
#   When you need a demo or internal tool around the agent. Skip for API-only
#   products.
#
# Why it matters
#   - A "talk to it" surface turns abstract architecture into "watch this work"
#     - critical for both internal demos and portfolio reviews.
#   - Talking to the API over HTTP enforces the same contract clients use; no
#     in-process shortcuts that hide bugs.
#   - Containerized separately keeps the UI's heavy frontend deps out of the
#     API image.
#
# What goes in it (Streamlit pattern)
#   - Read `API_URL` from env.
#   - Maintain `messages` in session state.
#   - Render existing turns with `st.chat_message(...)`.
#   - On submit: POST to `<API_URL>/v1/chat`, append response, render it.
#   - Surface citations and trace_id for debuggability.
#
# Example (commented)
#
#   API = os.getenv("API_URL", "http://app:8000")
#   st.title("<your project>")
#   if "messages" not in st.session_state:
#       st.session_state.messages = []
#   for m in st.session_state.messages:
#       st.chat_message(m["role"]).write(m["content"])
#   if prompt := st.chat_input("Ask something"):
#       st.session_state.messages.append({"role": "user", "content": prompt})
#       resp = httpx.post(f"{API}/v1/chat", json={"messages": st.session_state.messages}, timeout=30)
#       answer = resp.json().get("answer", "(no answer)")
#       st.session_state.messages.append({"role": "assistant", "content": answer})
#       st.chat_message("assistant").write(answer)
