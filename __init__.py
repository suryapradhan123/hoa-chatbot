"""
HOA Chatbot - Document-based Q&A system for Condominium Associations
"""

__version__ = "1.0.0"
__author__ = "suryapradhan123"

from .chatbot import HOAChatbot
from .document_processor import DocumentProcessor

__all__ = ["HOAChatbot", "DocumentProcessor"]
