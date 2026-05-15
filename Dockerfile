FROM python:3.11-slim

WORKDIR /app

# Dependências do sistema (Pillow precisa de algumas libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Diretório de saída dos criativos
RUN mkdir -p artifacts/outputs artifacts/images artifacts/logs

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
