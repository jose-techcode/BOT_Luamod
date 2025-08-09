import os
from dotenv import load_dotenv

# Get variables from the .env environment

load_dotenv()

# Load variables from the .env environment

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("DEV_ID")) # only for those who developed the bot or clone the repository
API_KEY_OPEN_ROUTER = os.getenv("API_KEY_OPEN_ROUTER") # only for those who developed the bot or clone the repository