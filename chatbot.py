"""
Chatbot implementation using RAG (Retrieval Augmented Generation)
"""
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from config import settings
from document_processor import DocumentProcessor


class HOAChatbot:
    """HOA Chatbot using RAG for document-based Q&A"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=settings.openai_api_key
        )
        self.document_processor = DocumentProcessor()
        self.document_processor.load_vector_store()
        
        # Custom prompt template
        self.qa_prompt = PromptTemplate(
            template="""You are a helpful assistant for a Condominium Homeowners Association (HOA/Condo Association).
Your role is to answer questions from condo owners about the community's bylaws, rules and regulations, 
shuttle schedules, replacement parts, and other community-related information.

Use the following pieces of context from the official documents to answer the question at the end.
If you don't know the answer based on the provided context, just say that you don't have that information 
in the documents, don't try to make up an answer.

Always be polite, professional, and helpful. If appropriate, suggest that the owner contact the 
management office for more specific assistance.

Context: {context}

Question: {question}

Helpful Answer:""",
            input_variables=["context", "question"]
        )
        
    def create_conversation_chain(self, session_id: str = "default"):
        """Create a conversational chain with memory"""
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        retriever = self.document_processor.get_retriever()
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt}
        )
        
        return chain
    
    def ask(self, question: str, session_id: str = "default") -> Dict:
        """
        Ask a question and get an answer
        
        Args:
            question: The user's question
            session_id: Session identifier for maintaining conversation context
            
        Returns:
            Dictionary with answer and source documents
        """
        try:
            chain = self.create_conversation_chain(session_id)
            result = chain({"question": question})
            
            return {
                "answer": result["answer"],
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "source": doc.metadata.get("source", "Unknown")
                    }
                    for doc in result.get("source_documents", [])
                ]
            }
        except Exception as e:
            return {
                "answer": f"I'm sorry, I encountered an error: {str(e)}",
                "source_documents": []
            }
