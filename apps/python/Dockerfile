FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instala somente as dependências solicitadas pelo app da aula.
COPY requirements-*.txt ./requirements/
ARG PYTHON_REQUIREMENTS=requirements-rag.txt
RUN python -m pip install --no-cache-dir -r /app/requirements/${PYTHON_REQUIREMENTS}

# O código da aplicação será montado/copiado ao incorporar o app correspondente.
