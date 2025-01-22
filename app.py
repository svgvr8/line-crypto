import os
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
from config import Config
from line_bot import LineMessageHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.SESSION_SECRET

# LINE Bot configuration
if not Config.LINE_CHANNEL_ACCESS_TOKEN:
    logger.error("LINE_CHANNEL_ACCESS_TOKEN is not set")
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is required")

logger.debug(f"Initializing LINE Bot API with token length: {len(Config.LINE_CHANNEL_ACCESS_TOKEN)}")
line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
message_handler = LineMessageHandler(line_bot_api)

@app.route("/")
def index():
    """Render status page"""
    return render_template('index.html', basic_id=Config.BASIC_ID)

@app.route("/callback", methods=['POST'])
def callback():
    """Handle LINE webhook callback"""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logger.debug(f"Request body: {body}")
    logger.debug(f"Signature: {signature}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature error")
        abort(400)
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        abort(500)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle incoming messages using LineMessageHandler"""
    try:
        logger.debug(f"Received message: {event.message.text}")
        # Use the message handler to process the message
        response = message_handler.handle_text_message(event)
        if response:
            line_bot_api.reply_message(event.reply_token, response)
            logger.debug(f"Sent response for message: {event.message.text}")
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        # Send a default error message to the user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later.")
        )

    return 'OK'