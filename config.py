import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    BASIC_ID = os.getenv('LINE_BASIC_ID', '')
    SESSION_SECRET = os.getenv('SESSION_SECRET', 'your-secret-key')
