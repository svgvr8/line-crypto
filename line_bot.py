"""
LINE Bot message handling and business logic module.
Handles different types of messages and provides business profile responses.
"""

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    PostbackAction, URIAction,
    CarouselTemplate, CarouselColumn,
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
        """
        Handle text messages and provide appropriate responses
        based on keywords and business logic
        """
        message_text = event.message.text.lower()
        user_id = event.source.user_id

        try:
            # Handle different message keywords
            if message_text in ['hi', 'hello', 'hey']:
                return self._handle_greeting()
            elif message_text == 'wallet':
                return self._handle_wallet_menu()
            elif message_text == 'create wallet':
                return self._handle_create_wallet(user_id)
            elif message_text == 'show wallet':
                return self._handle_show_wallet(user_id)
            elif 'hours' in message_text or 'opening' in message_text:
                return self._handle_business_hours()
            elif 'location' in message_text or 'address' in message_text:
                return self._handle_location()
            elif 'menu' in message_text or 'services' in message_text:
                return self._handle_services_menu()
            elif 'contact' in message_text:
                return self._handle_contact_info()
            else:
                return self._handle_default_response(message_text)

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return TextSendMessage(text="Sorry, I'm having trouble processing your request. Please try again later.")

    def _handle_greeting(self):
        """Handle greeting messages"""
        return TemplateSendMessage(
            alt_text="Welcome Menu",
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
                    ),
                    MessageAction(
                        label="Business Hours",
                        text="hours"
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
                text="What would you like to do with your wallet?",
                actions=[
                    MessageAction(
                        label="Create New Wallet",
                        text="create wallet"
                    ),
                    MessageAction(
                        label="Show My Wallet",
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

    def _handle_business_hours(self):
        """Handle business hours inquiries"""
        return TextSendMessage(
            text="Our business hours are:\n"
                 "Monday-Friday: 9:00 AM - 6:00 PM\n"
                 "Saturday: 10:00 AM - 4:00 PM\n"
                 "Sunday: Closed"
        )

    def _handle_location(self):
        """Handle location inquiries"""
        return TemplateSendMessage(
            alt_text="Business Location",
            template=ButtonsTemplate(
                title="Our Location",
                text="We are located at:\n123 Business Street\nCity, State 12345",
                actions=[
                    URIAction(
                        label="Open in Maps",
                        uri="https://www.google.com/maps"
                    )
                ]
            )
        )

    def _handle_services_menu(self):
        """Handle services menu display"""
        return TemplateSendMessage(
            alt_text="Our Services",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title="Service Category 1",
                        text="Professional consulting services",
                        actions=[
                            PostbackAction(
                                label="Learn More",
                                data="service_1"
                            )
                        ]
                    ),
                    CarouselColumn(
                        title="Service Category 2",
                        text="Business solutions",
                        actions=[
                            PostbackAction(
                                label="Learn More",
                                data="service_2"
                            )
                        ]
                    )
                ]
            )
        )

    def _handle_contact_info(self):
        """Handle contact information requests"""
        return TextSendMessage(
            text="Contact us at:\n"
                 "📞 Phone: (555) 123-4567\n"
                 "📧 Email: contact@business.com\n"
                 "💬 LINE: @business_account"
        )

    def _handle_default_response(self, message_text):
        """Handle default response for unrecognized messages"""
        return TemplateSendMessage(
            alt_text="Menu Options",
            template=ButtonsTemplate(
                title="Available Options",
                text="Here's what I can help you with:",
                actions=[
                    MessageAction(
                        label="Wallet Options",
                        text="wallet"
                    ),
                    MessageAction(
                        label="Business Hours",
                        text="hours"
                    ),
                    MessageAction(
                        label="Location",
                        text="location"
                    )
                ]
            )
        )