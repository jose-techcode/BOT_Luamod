import os
from dotenv import load_dotenv

# Pegar variáveis do ambiente .env

load_dotenv()

# Carregar variáveis do ambiente .env

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("DEV_ID"))