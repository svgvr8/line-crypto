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
            elif message_text == 'buy':
                return self._handle_buy()
            elif message_text == 'sell':
                return self._handle_sell()
            elif message_text == 'limit orders':
                return self._handle_limit_orders()
            elif message_text == 'dca':
                return self._handle_dca()
            elif message_text == 'withdraw':
                return self._handle_withdraw()
            elif message_text == 'settings':
                return self._handle_settings()
            else:
                return self._handle_trading_menu()

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later.")

    def _handle_greeting(self):
        """Handle greeting messages with trading options"""
        return self._handle_trading_menu()

    def _handle_trading_menu(self):
        """Show main trading menu"""
        return TemplateSendMessage(
            alt_text="Trading Menu",
            template=ButtonsTemplate(
                title="Atlas Trading Bot",
                text="Select an option:",
                actions=[
                    MessageAction(
                        label="Buy",
                        text="buy"
                    ),
                    MessageAction(
                        label="Sell",
                        text="sell"
                    ),
                    MessageAction(
                        label="More Options",
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
                            MessageAction(
                                label="Buy",
                                text="buy"
                            ),
                            MessageAction(
                                label="Sell",
                                text="sell"
                            ),
                            MessageAction(
                                label="More Options",
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
        """Handle wallet display with trading options"""
        try:
            wallet_info = self.wallet_handler.get_wallet(user_id)
            if wallet_info and wallet_info["status"] == "success":
                return TemplateSendMessage(
                    alt_text="Trading Options",
                    template=ButtonsTemplate(
                        title="Trading Options",
                        text=f"Address: {wallet_info['address'][:10]}...",
                        actions=[
                            MessageAction(
                                label="Limit Orders",
                                text="limit orders"
                            ),
                            MessageAction(
                                label="DCA",
                                text="dca"
                            ),
                            MessageAction(
                                label="Settings",
                                text="settings"
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

    def _handle_buy(self):
        """Handle buy action"""
        return TemplateSendMessage(
            alt_text="Buy Options",
            template=ButtonsTemplate(
                title="Buy Options",
                text="Select buy option:",
                actions=[
                    MessageAction(
                        label="Market Buy",
                        text="market buy"
                    ),
                    MessageAction(
                        label="Limit Buy",
                        text="limit orders"
                    ),
                    MessageAction(
                        label="Back to Menu",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_sell(self):
        """Handle sell action"""
        return TemplateSendMessage(
            alt_text="Sell Options",
            template=ButtonsTemplate(
                title="Sell Options",
                text="Select sell option:",
                actions=[
                    MessageAction(
                        label="Market Sell",
                        text="market sell"
                    ),
                    MessageAction(
                        label="Limit Sell",
                        text="limit orders"
                    ),
                    MessageAction(
                        label="Back to Menu",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_limit_orders(self):
        """Handle limit orders"""
        return TemplateSendMessage(
            alt_text="Limit Orders",
            template=ButtonsTemplate(
                title="⭕ Limit Orders",
                text="Set buy/sell limits:",
                actions=[
                    MessageAction(
                        label="Create Order",
                        text="create limit"
                    ),
                    MessageAction(
                        label="View Orders",
                        text="view limits"
                    ),
                    MessageAction(
                        label="Back",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_dca(self):
        """Handle DCA options"""
        return TemplateSendMessage(
            alt_text="DCA Options",
            template=ButtonsTemplate(
                title="📊 DCA",
                text="Manage DCA settings:",
                actions=[
                    MessageAction(
                        label="Setup DCA",
                        text="setup dca"
                    ),
                    MessageAction(
                        label="View DCA",
                        text="view dca"
                    ),
                    MessageAction(
                        label="Back",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_withdraw(self):
        """Handle withdrawal"""
        return TemplateSendMessage(
            alt_text="Withdraw",
            template=ButtonsTemplate(
                title="💰 Withdraw Funds",
                text="Select option:",
                actions=[
                    MessageAction(
                        label="Withdraw All",
                        text="withdraw all"
                    ),
                    MessageAction(
                        label="Custom Amount",
                        text="withdraw amount"
                    ),
                    MessageAction(
                        label="Back",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_settings(self):
        """Handle settings"""
        return TemplateSendMessage(
            alt_text="Settings",
            template=ButtonsTemplate(
                title="⚙️ Settings",
                text="Manage your settings:",
                actions=[
                    MessageAction(
                        label="Trading Settings",
                        text="trade settings"
                    ),
                    MessageAction(
                        label="Notifications",
                        text="notifications"
                    ),
                    MessageAction(
                        label="Back",
                        text="show wallet"
                    )
                ]
            )
        )