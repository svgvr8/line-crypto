import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '521f28d21adab2187b88c79ebb4e2a5a')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')  
    BASIC_ID = os.getenv('LINE_BASIC_ID', '2006965213')
    SESSION_SECRET = os.getenv('SESSION_SECRET', 'your-secret-key')