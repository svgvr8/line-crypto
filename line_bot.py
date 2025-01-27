"""
LINE Bot message handling for Wallet functionality
"""
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, CarouselTemplate, CarouselColumn,
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
            if message_text in ['hi', 'hello', 'hey']:
                return self._handle_greeting()
            elif message_text == 'create wallet':
                return self._handle_create_wallet(user_id)
            elif message_text == 'show wallet':
                return self._handle_show_wallet(user_id)
            else:
                return self._handle_trading_menu()

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later.")

    def _create_trading_carousel(self, address=None):
        """Create a carousel with all trading options"""
        columns = [
            # Trading Card
            CarouselColumn(
                title="Trading Options",
                text="Buy or Sell" if not address else f"Address: {address[:10]}...",
                actions=[
                    MessageAction(label="Buy", text="buy"),
                    MessageAction(label="Sell", text="sell"),
                    MessageAction(label="📊 DCA", text="dca")
                ]
            ),
            # Orders Card
            CarouselColumn(
                title="Order Management",
                text="Manage your orders",
                actions=[
                    MessageAction(label="⭕ Limit Orders", text="limit orders"),
                    MessageAction(label="📊 Positions", text="positions"),
                    MessageAction(label="💰 Withdraw", text="withdraw")
                ]
            ),
            # Settings Card
            CarouselColumn(
                title="Settings & Help",
                text="Additional options",
                actions=[
                    MessageAction(label="⚙️ Settings", text="settings"),
                    MessageAction(label="🔗 Referrals", text="referrals"),
                    MessageAction(label="❓ Help", text="help")
                ]
            )
        ]
        return CarouselTemplate(columns=columns)

    def _handle_greeting(self):
        """Handle greeting messages with trading options"""
        return TemplateSendMessage(
            alt_text="Trading Menu",
            template=self._create_trading_carousel()
        )

    def _handle_create_wallet(self, user_id):
        """Handle wallet creation"""
        try:
            wallet_info = self.wallet_handler.create_wallet(user_id)
            if wallet_info["status"] == "success":
                return TemplateSendMessage(
                    alt_text="Trading Menu",
                    template=self._create_trading_carousel(wallet_info['address'])
                )
            else:
                return TextSendMessage(text=wallet_info["message"])
        except Exception as e:
            logger.error(f"Error creating wallet: {str(e)}")
            return TextSendMessage(
                text="Sorry, there was an error creating your wallet. Please try again later."
            )

    def _handle_show_wallet(self, user_id):
        """Handle wallet display with trading options"""
        try:
            wallet_info = self.wallet_handler.get_wallet(user_id)
            if wallet_info and wallet_info["status"] == "success":
                return TemplateSendMessage(
                    alt_text="Trading Menu",
                    template=self._create_trading_carousel(wallet_info['address'])
                )
            else:
                return TemplateSendMessage(
                    alt_text="No Wallet",
                    template=CarouselTemplate(columns=[
                        CarouselColumn(
                            title="No Wallet Found",
                            text="Create a wallet to start trading",
                            actions=[
                                MessageAction(label="Create Wallet", text="create wallet"),
                                MessageAction(label="Learn More", text="help"),
                                MessageAction(label="Main Menu", text="menu")
                            ]
                        )
                    ])
                )
        except Exception as e:
            logger.error(f"Error showing wallet: {str(e)}")
            return TextSendMessage(
                text="Sorry, there was an error retrieving your wallet information. Please try again later."
            )

    def _handle_trading_menu(self):
        """Show main trading menu"""
        return TemplateSendMessage(
            alt_text="Trading Menu",
            template=self._create_trading_carousel()
        )