import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_TIMEOUT = 15
DATA_FILE = "data.json"
CHECK_INTERVAL = 60
