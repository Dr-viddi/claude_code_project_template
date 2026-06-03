# frontend/Dockerfile
#
# Purpose
#   Container image for the optional UI. Built and scaled independently of the
#   API so the two evolve on their own schedules.
#
# When you want a file like this
#   Any project with a UI you'll deploy. If the UI lives only as a local dev
#   script, skip it.
#
# Why it matters
#   - Same layer-caching hygiene as the API Dockerfile.
#   - Independent scaling: a viral demo can scale the UI horizontally without
#     touching the API.
#
# What goes in it
#   - Slim Python base.
#   - Standard env.
#   - Pip install from frontend/requirements.txt.
#   - EXPOSE the framework's default port (Streamlit: 8501; Next.js: 3000).
#   - CMD that binds to 0.0.0.0.
#
# Example (commented; Streamlit)
#
# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
# WORKDIR /srv
# COPY frontend/requirements.txt ./
# RUN pip install --upgrade pip && pip install -r requirements.txt
# COPY frontend/app.py ./
# EXPOSE 8501
# CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
