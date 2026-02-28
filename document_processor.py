"""
Document ingestion and processing for HOA Chatbot
"""
import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

from config import settings


class DocumentProcessor:
    """Handles document loading, processing, and indexing"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None
        
    def load_documents(self, directory_path: str = None) -> List[Document]:
        """Load documents from the specified directory"""
        if directory_path is None:
            directory_path = settings.documents_path
            
        documents = []
        
        # Create directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)
        
        # Load PDF files
        try:
            pdf_loader = DirectoryLoader(
                directory_path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                show_progress=True
            )
            documents.extend(pdf_loader.load())
        except Exception as e:
            print(f"Error loading PDFs: {e}")
        
        # Load text files
        try:
            txt_loader = DirectoryLoader(
                directory_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents.extend(txt_loader.load())
        except Exception as e:
            print(f"Error loading text files: {e}")
        
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)
    
    def create_vector_store(self, documents: List[Document]):
        """Create or update the vector store with processed documents"""
        if not documents:
            print("No documents to process")
            return
        
        # Create the Chroma vector store
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=settings.chroma_db_path
        )
        print(f"Created vector store with {len(documents)} document chunks")
        
    def load_vector_store(self):
        """Load existing vector store"""
        if os.path.exists(settings.chroma_db_path):
            self.vector_store = Chroma(
                persist_directory=settings.chroma_db_path,
                embedding_function=self.embeddings
            )
            print("Loaded existing vector store")
        else:
            print("No existing vector store found")
    
    def ingest_documents(self):
        """Complete document ingestion pipeline"""
        print(f"Loading documents from {settings.documents_path}...")
        documents = self.load_documents()
        
        if not documents:
            print("No documents found to ingest")
            return
        
        print(f"Loaded {len(documents)} documents")
        print("Processing documents...")
        processed_docs = self.process_documents(documents)
        
        print(f"Creating vector store with {len(processed_docs)} chunks...")
        self.create_vector_store(processed_docs)
        print("Document ingestion complete!")
        
    def get_retriever(self, k: int = 4):
        """Get a retriever for the vector store"""
        if self.vector_store is None:
            self.load_vector_store()
        
        if self.vector_store is None:
            raise ValueError("No vector store available. Please ingest documents first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
