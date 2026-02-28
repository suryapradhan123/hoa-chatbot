"""
WhatsApp integration using Twilio for HOA Chatbot
"""
from fastapi import APIRouter, Request, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from typing import Optional
import logging

from chatbot import HOAChatbot
from config import settings

logger = logging.getLogger(__name__)

# Create router for WhatsApp endpoints
whatsapp_router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# Initialize Twilio client
twilio_client = None
if settings.twilio_account_sid and settings.twilio_auth_token:
    try:
        twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        logger.info("Twilio client initialized successfully")
    except Exception as e:
        logger.warning(f"Could not initialize Twilio client: {e}")

# Chatbot instance
chatbot = None


def get_chatbot():
    """Get or create chatbot instance"""
    global chatbot
    if chatbot is None:
        chatbot = HOAChatbot()
    return chatbot


@whatsapp_router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...),
    To: Optional[str] = Form(None),
    MessageSid: Optional[str] = Form(None)
):
    """
    WhatsApp webhook endpoint for receiving messages from Twilio
    
    This endpoint receives incoming WhatsApp messages, processes them through the chatbot,
    and sends back responses.
    
    Args:
        Body: The message text from the user
        From: The sender's WhatsApp number
        To: The recipient's WhatsApp number (bot)
        MessageSid: Unique message identifier
        
    Returns:
        TwiML response with the chatbot's answer
    """
    logger.info(f"Received WhatsApp message from {From}: {Body}")
    
    # Create TwiML response
    twiml_response = MessagingResponse()
    
    try:
        # Get chatbot instance
        bot = get_chatbot()
        
        # Use the sender's number as session ID for conversation continuity
        session_id = From.replace("whatsapp:", "")
        
        # Get answer from chatbot
        result = bot.ask(Body, session_id=session_id)
        answer = result["answer"]
        
        # Add answer to response
        twiml_response.message(answer)
        
        logger.info(f"Sent response to {From}: {answer[:100]}...")
        
    except Exception as e:
        error_message = "I'm sorry, I encountered an error processing your question. Please try again later."
        twiml_response.message(error_message)
        logger.error(f"Error processing WhatsApp message: {e}")
    
    # Return TwiML response
    return Response(content=str(twiml_response), media_type="application/xml")


@whatsapp_router.get("/status")
async def whatsapp_status():
    """Check WhatsApp integration status"""
    return {
        "twilio_configured": twilio_client is not None,
        "chatbot_ready": chatbot is not None,
        "webhook_url": "/whatsapp/webhook"
    }


def send_whatsapp_message(to: str, message: str) -> bool:
    """
    Send a WhatsApp message using Twilio
    
    Args:
        to: Recipient's WhatsApp number (format: whatsapp:+1234567890)
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    if not twilio_client:
        logger.error("Twilio client not initialized")
        return False
    
    try:
        sent_message = twilio_client.messages.create(
            body=message,
            from_=settings.twilio_whatsapp_number,
            to=to
        )
        logger.info(f"Sent WhatsApp message to {to}, SID: {sent_message.sid}")
        return True
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return False
