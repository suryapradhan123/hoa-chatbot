"""
REST API for HOA Chatbot using FastAPI
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from chatbot import HOAChatbot
from document_processor import DocumentProcessor
from whatsapp_integration import whatsapp_router
from config import settings


app = FastAPI(
    title="HOA Chatbot API",
    description="REST API for Condominium Association Chatbot",
    version="1.0.0"
)

# Include WhatsApp router
app.include_router(whatsapp_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = None


class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str
    session_id: Optional[str] = "default"


class QuestionResponse(BaseModel):
    """Response model for question answers"""
    answer: str
    source_documents: List[Dict[str, str]]


class IngestRequest(BaseModel):
    """Request model for document ingestion"""
    documents_path: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize chatbot on startup"""
    global chatbot
    try:
        chatbot = HOAChatbot()
        print("Chatbot initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize chatbot: {e}")
        print("Please ingest documents first using POST /ingest")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HOA Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "ask": "POST /ask - Ask a question",
            "ingest": "POST /ingest - Ingest documents",
            "health": "GET /health - Health check",
            "whatsapp_webhook": "POST /whatsapp/webhook - WhatsApp integration webhook",
            "whatsapp_status": "GET /whatsapp/status - WhatsApp status"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chatbot_ready": chatbot is not None
    }


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question to the chatbot
    
    Args:
        request: Question request with question text and optional session_id
        
    Returns:
        Answer with source documents
    """
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot not initialized. Please ingest documents first."
        )
    
    try:
        result = chatbot.ask(request.question, request.session_id)
        return QuestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
async def ingest_documents(request: IngestRequest = None):
    """
    Ingest documents from the specified directory
    
    Args:
        request: Optional request with custom documents path
        
    Returns:
        Success message
    """
    global chatbot
    
    try:
        processor = DocumentProcessor()
        
        if request and request.documents_path:
            # Use custom path if provided
            documents = processor.load_documents(request.documents_path)
        else:
            # Use default path from settings
            processor.ingest_documents()
        
        # Reinitialize chatbot with new documents
        chatbot = HOAChatbot()
        
        return {
            "message": "Documents ingested successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_server():
    """Start the FastAPI server"""
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
