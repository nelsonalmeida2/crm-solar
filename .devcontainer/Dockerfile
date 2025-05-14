FROM python:3.11-slim

# Define o diretório de trabalho (dentro do container)
WORKDIR /app

# Instala dependências do sistema (PostgreSQL e ferramentas úteis)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    && apt-get clean

# Atualiza o pip
RUN pip install --upgrade pip

# Copia os ficheiros do projeto para o container
COPY . .

# (Opcional) Instala dependências Python automaticamente se existir requirements.txt
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
