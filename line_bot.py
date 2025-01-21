"""
LINE Bot message handling for DOSI Wallet integration
"""
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    PostbackAction, URIAction,
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
            elif message_text == 'dosi':
                return self._handle_dosi_menu()
            elif message_text == 'connect dosi':
                return self._handle_connect_dosi(user_id)
            elif message_text == 'check balance':
                return self._handle_dosi_balance(user_id)
            else:
                return self._handle_default_response()

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later.")

    def _handle_greeting(self):
        """Handle greeting messages with DOSI options"""
        return TemplateSendMessage(
            alt_text="Welcome to DOSI Wallet",
            template=ButtonsTemplate(
                title="Welcome to DOSI Wallet!",
                text="What would you like to do?",
                actions=[
                    MessageAction(
                        label="🔗 Connect DOSI",
                        text="connect dosi"
                    ),
                    MessageAction(
                        label="💰 Check Balance",
                        text="check balance"
                    ),
                    MessageAction(
                        label="📱 DOSI Menu",
                        text="dosi"
                    )
                ]
            )
        )

    def _handle_dosi_menu(self):
        """Handle DOSI wallet menu display"""
        return TemplateSendMessage(
            alt_text="DOSI Menu",
            template=ButtonsTemplate(
                title="DOSI Wallet Options",
                text="Choose an option:",
                actions=[
                    MessageAction(
                        label="🔗 Connect Wallet",
                        text="connect dosi"
                    ),
                    MessageAction(
                        label="💰 Check Balance",
                        text="check balance"
                    ),
                    URIAction(
                        label="📱 DOSI World",
                        uri="https://citizen.dosi.world"
                    )
                ]
            )
        )

    def _handle_connect_dosi(self, user_id):
        """Handle DOSI wallet connection"""
        wallet_info = self.wallet_handler.get_dosi_wallet(user_id)
        return TemplateSendMessage(
            alt_text="Connect DOSI Wallet",
            template=ButtonsTemplate(
                title="Connect DOSI Wallet",
                text="Connect your DOSI wallet to access your balance and assets",
                actions=[
                    URIAction(
                        label="🔗 Connect Now",
                        uri="https://citizen.dosi.world/login"
                    ),
                    MessageAction(
                        label="⬅️ Back to Menu",
                        text="dosi"
                    )
                ]
            )
        )

    def _handle_dosi_balance(self, user_id):
        """Handle DOSI balance check"""
        balance_info = self.wallet_handler.get_dosi_balance(user_id)
        if balance_info["status"] == "success":
            return TextSendMessage(
                text=f"💰 DOSI Balance:\n{balance_info['balance']}\n\n"
                     f"To view your complete balance and assets, please use the DOSI app."
            )
        else:
            return TemplateSendMessage(
                alt_text="DOSI Balance Error",
                template=ButtonsTemplate(
                    title="Connect DOSI First",
                    text="Please connect your DOSI wallet to check your balance",
                    actions=[
                        MessageAction(
                            label="🔗 Connect DOSI",
                            text="connect dosi"
                        )
                    ]
                )
            )

    def _handle_default_response(self):
        """Handle default response"""
        return TemplateSendMessage(
            alt_text="DOSI Options",
            template=ButtonsTemplate(
                title="DOSI Wallet",
                text="Here's what I can help you with:",
                actions=[
                    MessageAction(
                        label="💰 DOSI Menu",
                        text="dosi"
                    ),
                    MessageAction(
                        label="🔗 Connect Wallet",
                        text="connect dosi"
                    ),
                    MessageAction(
                        label="💳 Check Balance",
                        text="check balance"
                    )
                ]
            )
        )

    def _handle_wallet_menu(self):
        """Handle wallet menu display"""
        return TemplateSendMessage(
            alt_text="Wallet Menu",
            template=ButtonsTemplate(
                title="Wallet Options",
                text="Choose an option:",
                thumbnail_image_url="https://img.icons8.com/color/96/000000/wallet.png",
                actions=[
                    MessageAction(
                        label="💰 Create New Wallet",
                        text="create wallet"
                    ),
                    MessageAction(
                        label="👁️ Show My Wallet",
                        text="show wallet"
                    )
                ]
            )
        )

    def _handle_create_wallet(self, user_id):
        """Handle wallet creation"""
        try:
            wallet_info = self.wallet_handler.create_wallet(user_id)
            return TextSendMessage(
                text=f"✅ Wallet created successfully!\n\n"
                     f"📝 Address: {wallet_info['address']}\n\n"
                     f"🔐 Private Key: {wallet_info['private_key']}\n\n"
                     f"⚠️ Keep your private key safe and never share it!"
            )
        except Exception as e:
            logger.error(f"Error creating wallet: {str(e)}")
            return TextSendMessage(
                text="Sorry, there was an error creating your wallet. Please try again later."
            )

    def _handle_show_wallet(self, user_id):
        """Handle wallet display"""
        wallet_info = self.wallet_handler.get_wallet(user_id)
        if wallet_info:
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
                            label="Create Wallet",
                            text="create wallet"
                        )
                    ]
                )
            )