FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# COPY .env .env
# COPY firebase-credentials.json firebase-credentials.json

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]