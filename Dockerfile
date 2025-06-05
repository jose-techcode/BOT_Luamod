# Usa uma imagem oficial do Python
FROM python:3.12-slim

# Define o diretório dentro do container
WORKDIR /app

# Copia todos os arquivos da sua pasta local para o container (. significa "essa pasta")
COPY . /app

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Comando para rodar o bot
CMD ["python", "bot.py"]
