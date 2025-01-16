import os
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.SESSION_SECRET

# LINE Bot configuration
line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

@app.route("/")
def index():
    """Render status page"""
    return render_template('index.html', basic_id=Config.BASIC_ID)

@app.route("/callback", methods=['POST'])
def callback():
    """Handle LINE webhook callback"""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature error")
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle incoming messages"""
    try:
        # Echo the received message
        message_text = event.message.text
        response = TextSendMessage(text=f"You said: {message_text}")
        line_bot_api.reply_message(event.reply_token, response)
        
        logger.debug(f"Processed message: {message_text}")
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
