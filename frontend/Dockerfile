FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

COPY frontend/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY frontend/app.py ./
COPY frontend/static ./static

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
