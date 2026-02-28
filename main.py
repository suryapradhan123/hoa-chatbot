"""
Main entry point for HOA Chatbot
"""
import argparse
import sys
from document_processor import DocumentProcessor
from api import start_server


def ingest_documents():
    """Ingest documents into the vector database"""
    print("Starting document ingestion...")
    processor = DocumentProcessor()
    processor.ingest_documents()
    print("Document ingestion completed!")


def start_api_server():
    """Start the REST API server"""
    print("Starting HOA Chatbot API server...")
    start_server()


def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(description="HOA Chatbot - Document-based Q&A System")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Ingest command
    subparsers.add_parser("ingest", help="Ingest documents into the vector database")
    
    # Serve command
    subparsers.add_parser("serve", help="Start the REST API server")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        ingest_documents()
    elif args.command == "serve":
        start_api_server()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
