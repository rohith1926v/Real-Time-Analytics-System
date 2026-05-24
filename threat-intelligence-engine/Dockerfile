FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY threat-intelligence-engine/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY threat-intelligence-engine/app ./app
COPY detections/rules ./rules

CMD ["python", "-m", "app.main"]
