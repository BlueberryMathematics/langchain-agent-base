"""
RAG (Retrieval-Augmented Generation) Manager
============================================

Class-based RAG system for document indexing and retrieval.
Supports web scraping, document loading, and vector search.
"""

import os
import bs4
from typing import List, Optional, Dict, Any
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import create_retriever_tool
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class RAGManager:
    """
    Manages document indexing and retrieval for RAG applications.
    
    Features:
    - Web scraping and document loading
    - Text splitting and chunking
    - Vector embedding and storage
    - Retrieval tool creation
    """
    
    def __init__(self, 
                 embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 vector_size: int = 384):
        """
        Initialize the RAG manager.
        
        Args:
            embedding_model_name: HuggingFace embedding model name
            chunk_size: Size of document chunks
            chunk_overlap: Overlap between chunks
            vector_size: Dimension of embedding vectors
        """
        self.embedding_model_name = embedding_model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_size = vector_size
        
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        
        # In-memory Qdrant client
        self.client = QdrantClient(":memory:")
        self.collections = {}
    
    async def setup_from_urls(self, 
                            urls: List[str], 
                            collection_name: str = "web_docs",
                            css_selector: Dict[str, Any] = None) -> List:
        """
        Setup RAG from web URLs.
        
        Args:
            urls: List of URLs to scrape
            collection_name: Name for the vector collection
            css_selector: CSS selector configuration for scraping
        
        Returns:
            List of retriever tools
        """
        if css_selector is None:
            css_selector = dict(
                class_=("post-content", "post-title", "post-header", "article", "content")
            )
        
        # Load documents from URLs
        loader = WebBaseLoader(
            web_paths=tuple(urls),
            bs_kwargs=dict(parse_only=bs4.SoupStrainer(**css_selector))
        )
        docs = await loader.aload()
        
        return await self._setup_collection(docs, collection_name)
    
    async def setup_from_documents(self, 
                                 documents: List[str], 
                                 collection_name: str = "text_docs") -> List:
        """
        Setup RAG from text documents.
        
        Args:
            documents: List of document texts
            collection_name: Name for the vector collection
        
        Returns:
            List of retriever tools
        """
        # Convert strings to Document objects
        docs = [Document(page_content=doc) for doc in documents]
        
        return await self._setup_collection(docs, collection_name)
    
    async def _setup_collection(self, docs: List[Document], collection_name: str) -> List:
        """
        Internal method to setup a vector collection.
        
        Args:
            docs: List of documents to index
            collection_name: Name for the collection
        
        Returns:
            List of retriever tools
        """
        if not docs:
            return []
        
        # Split documents
        splits = self.text_splitter.split_documents(docs)
        
        # Create collection if it doesn't exist
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )
        except Exception as e:
            # Collection might already exist
            pass
        
        # Create vector store
        vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embedding_model,
        )
        
        # Add documents
        await vectorstore.aadd_documents(splits)
        
        # Store collection reference
        self.collections[collection_name] = vectorstore
        
        # Create retriever tool
        retriever = vectorstore.as_retriever()
        
        retriever_tool = create_retriever_tool(
            retriever,
            f"search_{collection_name}",
            f"Search for information in the {collection_name} knowledge base."
        )
        
        return [retriever_tool]
    
    def add_documents_to_collection(self, 
                                  documents: List[str], 
                                  collection_name: str) -> None:
        """
        Add more documents to an existing collection.
        
        Args:
            documents: List of document texts to add
            collection_name: Name of the existing collection
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection {collection_name} not found")
        
        docs = [Document(page_content=doc) for doc in documents]
        splits = self.text_splitter.split_documents(docs)
        
        # Add to existing vectorstore
        vectorstore = self.collections[collection_name]
        vectorstore.add_documents(splits)
    
    def list_collections(self) -> List[str]:
        """Get list of available collections."""
        return list(self.collections.keys())
    
    def get_retriever(self, collection_name: str):
        """Get a retriever for a specific collection."""
        if collection_name not in self.collections:
            raise ValueError(f"Collection {collection_name} not found")
        
        return self.collections[collection_name].as_retriever()


# Backward compatibility function
async def setup_rag_tools():
    """Legacy function for backward compatibility."""
    manager = RAGManager()
    return await manager.setup_from_urls([
        "https://blog.langchain.com/langchain-langgraph-1dot0/"
    ], "langchain_blog")
