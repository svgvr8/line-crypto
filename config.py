import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    BASIC_ID = os.environ.get('LINE_BASIC_ID')
    SESSION_SECRET = os.environ.get('SESSION_SECRET', 'your-secret-key')