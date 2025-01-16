"""
LINE Bot message handling and business logic module.
Handles different types of messages and provides business profile responses.
"""

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    PostbackAction, URIAction,
    CarouselTemplate, CarouselColumn
)
import logging

logger = logging.getLogger(__name__)

class LineMessageHandler:
    def __init__(self, line_bot_api):
        """Initialize the message handler with LINE Bot API instance"""
        self.line_bot_api = line_bot_api
        
    def handle_text_message(self, event):
        """
        Handle text messages and provide appropriate responses
        based on keywords and business logic
        """
        message_text = event.message.text.lower()
        
        try:
            # Handle different message keywords
            if message_text in ['hi', 'hello', 'hey']:
                return self._handle_greeting()
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
        return TextSendMessage(
            text="Hello! Welcome to our business. How can I help you today?\n"
                 "You can ask about our:\n"
                 "• Business Hours\n"
                 "• Location\n"
                 "• Services\n"
                 "• Contact Information"
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
        return TextSendMessage(
            text=f"Thanks for your message: '{message_text}'\n"
                 "I can help you with:\n"
                 "• Business Hours\n"
                 "• Location\n"
                 "• Services\n"
                 "• Contact Information\n"
                 "Please let me know what you'd like to know more about!"
        )
