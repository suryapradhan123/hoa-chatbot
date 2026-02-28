"""
Example usage script demonstrating HOA Chatbot API
"""

# Example 1: Using the chatbot via Python
def example_python_usage():
    """
    Example: Using the chatbot directly in Python code
    (Requires OPENAI_API_KEY in .env)
    """
    from chatbot import HOAChatbot
    
    # Initialize chatbot
    bot = HOAChatbot()
    
    # Ask questions
    questions = [
        "What are the quiet hours?",
        "When is the shuttle to downtown?",
        "What is the pet policy?",
        "Who do I contact for appliance replacement?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        result = bot.ask(question)
        print(f"A: {result['answer']}\n")


# Example 2: Using the REST API
def example_rest_api():
    """
    Example: Making requests to the REST API
    """
    import requests
    
    base_url = "http://localhost:8000"
    
    # Health check
    response = requests.get(f"{base_url}/health")
    print("Health check:", response.json())
    
    # Ask a question
    question_data = {
        "question": "What are the pool hours?",
        "session_id": "user123"
    }
    response = requests.post(f"{base_url}/ask", json=question_data)
    result = response.json()
    
    print(f"\nQuestion: {question_data['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {len(result['source_documents'])} documents")


# Example 3: Using curl commands
CURL_EXAMPLES = """
# Example curl commands for testing the API

# 1. Health check
curl http://localhost:8000/health

# 2. Ask a question
curl -X POST "http://localhost:8000/ask" \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "What are the quiet hours?",
    "session_id": "user123"
  }'

# 3. Ingest documents
curl -X POST "http://localhost:8000/ingest"

# 4. Check WhatsApp status
curl http://localhost:8000/whatsapp/status

# 5. Test with different questions
curl -X POST "http://localhost:8000/ask" \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "When is the shuttle to the shopping district?",
    "session_id": "user456"
  }'

curl -X POST "http://localhost:8000/ask" \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "What is the pet weight limit?",
    "session_id": "user789"
  }'

curl -X POST "http://localhost:8000/ask" \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "Who should I contact for a refrigerator replacement?",
    "session_id": "user101"
  }'
"""


if __name__ == "__main__":
    print("=" * 60)
    print("HOA Chatbot - Example Usage")
    print("=" * 60)
    print()
    print("This file contains examples of how to use the HOA Chatbot.")
    print()
    print("Before running examples:")
    print("1. Ensure .env file has your OPENAI_API_KEY")
    print("2. Run: python main.py ingest")
    print("3. Run: python main.py serve")
    print()
    print("=" * 60)
    print("CURL Examples:")
    print("=" * 60)
    print(CURL_EXAMPLES)
    print()
    print("To run Python examples:")
    print("  - Uncomment example_python_usage() or example_rest_api()")
    print("  - Ensure dependencies are installed")
    print()
