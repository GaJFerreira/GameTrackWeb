FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Instala dependências do sistema e Python
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# --- ATENÇÃO: As linhas abaixo FORAM REMOVIDAS ---
# COPY .env .env
# COPY firebase-credentials.json firebase-credentials.json
# -------------------------------------------------
# O Render injeta essas informações automaticamente via Variáveis de Ambiente
# e Secret Files, então não precisamos (e não podemos) copiá-las aqui.

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]