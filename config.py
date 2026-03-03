import os
from dotenv import load_dotenv

# Lệnh này sẽ tự động đọc các biến bí mật trong file .env của bạn
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")