"""
LINE Bot message handling for Wallet functionality
"""
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    MessageAction
)
import logging
from wallet_handler import WalletHandler

logger = logging.getLogger(__name__)

class LineMessageHandler:
    def __init__(self, line_bot_api):
        """Initialize the message handler with LINE Bot API instance"""
        self.line_bot_api = line_bot_api
        self.wallet_handler = WalletHandler()

    def handle_text_message(self, event):
        """Handle text messages and provide appropriate responses"""
        message_text = event.message.text.lower()
        user_id = event.source.user_id

        try:
            logger.debug(f"Processing message: {message_text}")
            # Handle different message keywords
            if message_text in ['hi', 'hello', 'hey']:
                return self._handle_greeting()
            elif message_text == 'create wallet':
                return self._handle_create_wallet(user_id)
            elif message_text == 'show wallet':
                return self._handle_show_wallet(user_id)
            else:
                return self._handle_default_response()

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later.")

    def _handle_greeting(self):
        """Handle greeting messages with wallet options"""
        return TemplateSendMessage(
            alt_text="Welcome to Wallet Manager",
            template=ButtonsTemplate(
                title="Welcome to Wallet Manager!",
                text="What would you like to do?",
                actions=[
                    MessageAction(
                        label="💰 Create Wallet",
                        text="create wallet"
                    ),
                    MessageAction(
                        label="👁️ Show Wallet",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_create_wallet(self, user_id):
        """Handle wallet creation"""
        try:
            wallet_info = self.wallet_handler.create_wallet(user_id)
            if wallet_info["status"] == "success":
                return TextSendMessage(
                    text=f"✅ Wallet created successfully!\n\n"
                         f"📝 Address: {wallet_info['address']}\n\n"
                         f"🔐 Private Key: {wallet_info['private_key']}\n\n"
                         f"⚠️ IMPORTANT: Save your private key securely and never share it!"
                )
            else:
                return TextSendMessage(text=wallet_info["message"])
        except Exception as e:
            logger.error(f"Error creating wallet: {str(e)}")
            return TextSendMessage(
                text="Sorry, there was an error creating your wallet. Please try again later."
            )

    def _handle_show_wallet(self, user_id):
        """Handle wallet display"""
        try:
            wallet_info = self.wallet_handler.get_wallet(user_id)
            if wallet_info and wallet_info["status"] == "success":
                return TextSendMessage(
                    text=f"💳 Your Wallet Information:\n\n"
                         f"📝 Address: {wallet_info['address']}\n\n"
                         f"⚠️ Never share your private key with anyone!"
                )
            else:
                return TemplateSendMessage(
                    alt_text="No Wallet Found",
                    template=ButtonsTemplate(
                        title="No Wallet Found",
                        text="You don't have a wallet yet. Would you like to create one?",
                        actions=[
                            MessageAction(
                                label="💰 Create Wallet",
                                text="create wallet"
                            )
                        ]
                    )
                )
        except Exception as e:
            logger.error(f"Error showing wallet: {str(e)}")
            return TextSendMessage(
                text="Sorry, there was an error retrieving your wallet information. Please try again later."
            )

    def _handle_default_response(self):
        """Handle default response"""
        return TemplateSendMessage(
            alt_text="Wallet Options",
            template=ButtonsTemplate(
                title="Wallet Manager",
                text="Here's what I can help you with:",
                actions=[
                    MessageAction(
                        label="💰 Create Wallet",
                        text="create wallet"
                    ),
                    MessageAction(
                        label="👁️ Show Wallet",
                        text="show wallet"
                    )
                ]
            )
        )