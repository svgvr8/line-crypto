import os
from flask import Flask, request, abort, render_template, Response
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

if not Config.LINE_CHANNEL_SECRET:
    logger.error("LINE_CHANNEL_SECRET is not set")
    raise ValueError("LINE_CHANNEL_SECRET is required")

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
    if request.method != 'POST':
        return 'Method Not Allowed', 405

    # Get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature', '')

    # Get request body as text
    body = request.get_data(as_text=True)
    logger.debug(f"Request body: {body}")
    logger.debug(f"Signature: {signature}")

    try:
        handler.handle(body, signature)
        # Return OK with content type header to prevent default response
        return Response('OK', mimetype='text/plain', status=200)
    except InvalidSignatureError:
        logger.error("Invalid signature error")
        abort(400)
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        abort(500)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle incoming messages using LineMessageHandler"""
    try:
        logger.debug(f"Received message: {event.message.text}")
        # Use the message handler to process the message
        response = message_handler.handle_text_message(event)
        if response:
            # Reply with our custom message and prevent default response
            line_bot_api.reply_message(
                event.reply_token,
                response,
                notification_disabled=True  # This helps prevent additional notifications
            )
            logger.debug(f"Sent response for message: {event.message.text}")
            return Response('OK', mimetype='text/plain', status=200)
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        # Send a default error message to the user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later."),
            notification_disabled=True
        )
    return Response('OK', mimetype='text/plain', status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)