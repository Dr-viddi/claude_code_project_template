# frontend/Dockerfile
#
# Intention:
#   Container image for the UI. Built and scaled independently of the API.
#
# What this file should contain:
#   - Same hygiene as `app/Dockerfile` (slim base, env, layer ordering).
#   - Pip install from `frontend/requirements.txt`.
#   - Expose the framework's default port (Streamlit: 8501; Next.js: 3000).
#   - CMD that starts the framework bound to 0.0.0.0.
#
# Example (commented; Streamlit; remove the leading '#' to activate):
#
# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
# WORKDIR /srv
# COPY frontend/requirements.txt ./
# RUN pip install --upgrade pip && pip install -r requirements.txt
# COPY frontend/app.py ./
# COPY frontend/static ./static
# EXPOSE 8501
# CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
