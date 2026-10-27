# Usa uma imagem oficial e leve do Python
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e força o log em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema operacional necessárias para o OCR e compilações
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para iniciar o backend a partir da raiz do projeto
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]