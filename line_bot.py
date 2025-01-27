"""
LINE Bot message handling for Wallet functionality
"""
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    MessageAction, URIAction
)
import logging
from wallet_handler import WalletHandler
import os

logger = logging.getLogger(__name__)

class LineMessageHandler:
    def __init__(self, line_bot_api):
        """Initialize the message handler with LINE Bot API instance"""
        self.line_bot_api = line_bot_api
        self.wallet_handler = WalletHandler()
        self.base_url = f"https://{os.environ.get('REPL_SLUG')}.{os.environ.get('REPL_OWNER')}.repl.co"

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
            alt_text="Wallet Options",
            template=ButtonsTemplate(
                title="Welcome!",
                text="What would you like to do?",
                actions=[
                    MessageAction(
                        label="Create Wallet",
                        text="create wallet"
                    ),
                    MessageAction(
                        label="Show Wallet",
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
                return TemplateSendMessage(
                    alt_text="Wallet Created",
                    template=ButtonsTemplate(
                        title="Wallet Created!",
                        text=f"Address: {wallet_info['address'][:10]}...",
                        actions=[
                            URIAction(
                                label="Trade Now",
                                uri=f"{self.base_url}/trading/{user_id}"
                            ),
                            MessageAction(
                                label="Show Details",
                                text="show wallet"
                            )
                        ]
                    )
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
                return TemplateSendMessage(
                    alt_text="Wallet Info",
                    template=ButtonsTemplate(
                        title="Your Wallet",
                        text=f"Address: {wallet_info['address'][:10]}...",
                        actions=[
                            URIAction(
                                label="Trade Now",
                                uri=f"{self.base_url}/trading/{user_id}"
                            ),
                            MessageAction(
                                label="Refresh",
                                text="show wallet"
                            )
                        ]
                    )
                )
            else:
                return TemplateSendMessage(
                    alt_text="No Wallet",
                    template=ButtonsTemplate(
                        title="No Wallet Found",
                        text="Create a wallet?",
                        actions=[
                            MessageAction(
                                label="Create Wallet",
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
            alt_text="Options",
            template=ButtonsTemplate(
                title="Wallet Manager",
                text="Choose an option:",
                actions=[
                    MessageAction(
                        label="Create Wallet",
                        text="create wallet"
                    ),
                    MessageAction(
                        label="Show Wallet",
                        text="show wallet"
                    )
                ]
            )
        )