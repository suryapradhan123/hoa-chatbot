# HOA Chatbot

A Condominium Association ChatBot that uses RAG (Retrieval Augmented Generation) to answer questions from owners based on official documents like bylaws, rules and regulations, shuttle schedules, replacement parts information, and more.

## Features

- 🤖 **AI-Powered Q&A**: Uses OpenAI's GPT models with retrieval augmented generation for accurate, document-based answers
- 📄 **Document Ingestion**: Supports PDF and text files for easy knowledge base management
- 🔍 **Semantic Search**: ChromaDB vector store for efficient document retrieval
- 🌐 **REST API**: FastAPI-based REST API for easy integration
- 💬 **WhatsApp Integration**: Twilio-powered WhatsApp bot for conversational interaction
- 🔒 **Session Management**: Maintains conversation context for better user experience

## Architecture

```
┌─────────────────┐
│  Condo Owners   │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼──────┐
│ REST  │  │ WhatsApp│
│ API   │  │ (Twilio)│
└───┬───┘  └──┬──────┘
    │         │
    └────┬────┘
         │
    ┌────▼─────────┐
    │  HOA Chatbot │
    │  (LangChain) │
    └────┬─────────┘
         │
    ┌────┴─────────┐
    │ Vector Store │
    │  (ChromaDB)  │
    └──────────────┘
```

## Installation

### Prerequisites

- Python 3.8 to 3.12 (Python 3.13+ is not yet supported due to dependency compatibility)
- OpenAI API key
- (Optional) Twilio account for WhatsApp integration

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/suryapradhan123/hoa-chatbot.git
   cd hoa-chatbot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional: For WhatsApp integration
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

## Usage

### 1. Ingest Documents

Place your HOA documents (PDFs, text files) in the `documents/` directory, then run:

```bash
python main.py ingest
```

This will:
- Load all documents from the `documents/` directory
- Process and chunk the documents
- Create embeddings and store them in the ChromaDB vector database

### 2. Start the API Server

```bash
python main.py serve
```

The server will start at `http://localhost:8000`

### 3. API Endpoints

#### Ask a Question
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the quiet hours?",
    "session_id": "user123"
  }'
```

Response:
```json
{
  "answer": "The quiet hours are from 10:00 PM to 8:00 AM on weekdays and from 11:00 PM to 9:00 AM on weekends.",
  "source_documents": [
    {
      "content": "1. NOISE AND QUIET HOURS\n   - Quiet hours are from 10:00 PM to 8:00 AM on weekdays...",
      "source": "documents/rules_and_regulations.txt"
    }
  ]
}
```

#### Ingest Documents via API
```bash
curl -X POST "http://localhost:8000/ingest"
```

#### Health Check
```bash
curl http://localhost:8000/health
```

### 4. WhatsApp Integration

#### Setup Twilio WhatsApp

1. Create a Twilio account at https://www.twilio.com
2. Set up WhatsApp Sandbox or get approved WhatsApp Business number
3. Configure webhook URL in Twilio console:
   ```
   https://your-domain.com/whatsapp/webhook
   ```

#### Test WhatsApp Locally (using ngrok)

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Start the API server
python main.py serve

# In another terminal, expose local server
ngrok http 8000

# Copy the ngrok URL and set it in Twilio console
# https://abc123.ngrok.io/whatsapp/webhook
```

#### WhatsApp Status
```bash
curl http://localhost:8000/whatsapp/status
```

## Document Structure

Place your documents in the `documents/` directory:

```
documents/
├── bylaws.txt
├── rules_and_regulations.txt
├── shuttle_schedule.txt
├── replacement_parts.txt
└── other_documents.pdf
```

Supported formats:
- `.txt` - Plain text files
- `.pdf` - PDF documents

## Example Documents

The repository includes sample documents:
- **bylaws.txt**: Condominium association bylaws
- **rules_and_regulations.txt**: Community rules and policies
- **shuttle_schedule.txt**: Transportation schedules
- **replacement_parts.txt**: Approved vendors and parts information

## Example Questions

Try asking the chatbot:
- "What are the quiet hours?"
- "How do I reserve the shuttle?"
- "What is the pet policy?"
- "When is the annual meeting?"
- "Who should I contact for a dishwasher replacement?"
- "What are the pool hours?"

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key (required) | - |
| TWILIO_ACCOUNT_SID | Twilio account SID (optional) | - |
| TWILIO_AUTH_TOKEN | Twilio auth token (optional) | - |
| TWILIO_WHATSAPP_NUMBER | Twilio WhatsApp number (optional) | - |
| API_HOST | API server host | 0.0.0.0 |
| API_PORT | API server port | 8000 |
| DOCUMENTS_PATH | Path to documents directory | ./documents |
| CHROMA_DB_PATH | Path to ChromaDB storage | ./chroma_db |

## Development

### Project Structure

```
hoa-chatbot/
├── api.py                      # FastAPI REST API
├── chatbot.py                  # RAG chatbot implementation
├── config.py                   # Configuration management
├── document_processor.py       # Document ingestion & vector store
├── whatsapp_integration.py     # WhatsApp/Twilio integration
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── documents/                 # Document storage
│   ├── bylaws.txt
│   ├── rules_and_regulations.txt
│   └── ...
└── chroma_db/                 # Vector database (auto-created)
```

## Troubleshooting

**Issue**: "No vector store available"
- **Solution**: Run `python main.py ingest` to create the vector database

**Issue**: WhatsApp webhook not receiving messages
- **Solution**: Ensure your webhook URL is publicly accessible and correctly configured in Twilio

**Issue**: OpenAI API errors
- **Solution**: Check that your OPENAI_API_KEY is valid and has sufficient credits

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
- Create an issue on GitHub
- Contact: suryapradhan123

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
