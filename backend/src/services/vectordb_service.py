from abc import ABC, abstractmethod
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import chromadb
import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class DocumentChunk:
    id: str
    content: str
    metadata: Dict[str, Any]

@dataclass 
class SearchResult:
    chunk: DocumentChunk
    score: float

class VectorDBInterface(ABC):
    
    @abstractmethod
    async def add_documents(self, chunks: List[DocumentChunk]) -> bool:
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        pass

class ChromaVectorDB(VectorDBInterface):
    
    def __init__(self, host: str = "vector_db", port: int = 8000):
        self.host = host
        self.port = port
        self.client = None
        self.collection = None
        logger.info("Initializing HuggingFace Embeddings")
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        logger.info("HuggingFace Embeddings initialized")
        logger.info("Setting up text splitter")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    async def connect(self):
        logger.info(f"Connecting to ChromaDB at {self.host}:{self.port}")
        self.client = chromadb.HttpClient(host=self.host, port=self.port)
        self.collection = self.client.get_or_create_collection("documents")
        return True
    
    async def add_document(self, document_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Add a document by splitting it into chunks automatically"""
        logger.info(f"Adding document {document_id} to vector database")
        if not self.collection:
            await self.connect()
        logger.info(f"Adding document {document_id} to vector database")
        
        # Split the content into chunks
        documents = [Document(page_content=content, metadata=metadata)]
        docs = self.text_splitter.split_documents(documents)
        
        # Convert to DocumentChunk format
        chunks = []
        for i, doc in enumerate(docs):
            chunk = DocumentChunk(
                id=f"{document_id}_chunk_{i}",
                content=doc.page_content,
                metadata={**doc.metadata, "chunk_index": i, "document_id": document_id}
            )
            chunks.append(chunk)
        logger.info(f"Document split into {len(chunks)} chunks")
        # Use existing add_documents method
        return await self.add_documents(chunks)
    
    # Remove the duplicate method and keep only this one:
    async def add_documents(self, chunks: List[DocumentChunk]) -> bool:
        if not self.collection:
            await self.connect()
        
        # Generate embeddings with Mistral
        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        texts = [chunk.content for chunk in chunks]

        all_embeddings = await self.embeddings.aembed_documents(texts)
        
       

        logger.info(f"Generated embeddings for {len(chunks)} chunks")
        
        ids = [chunk.id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=all_embeddings
        )
        return True
    
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        if not self.collection:
            await self.connect()
        
        # Generate query embedding with Mistral
        query_embedding = await self.embeddings.aembed_query(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )
        
        search_results = []
        for i, doc_id in enumerate(results["ids"][0]):
            chunk = DocumentChunk(
                id=doc_id,
                content=results["documents"][0][i],
                metadata=results["metadatas"][0][i]
            )
            # Convert distance to similarity score (1 - distance)
            score = 1 - results["distances"][0][i] if "distances" in results else 1.0
            search_result = SearchResult(chunk=chunk, score=score)
            search_results.append(search_result)
        
        return search_results
    
    async def health_check(self) -> bool:
        try:
            if not self.client:
                await self.connect()
            self.client.heartbeat()
            return True
        except:
            return False

def get_vector_db() -> VectorDBInterface:
    return ChromaVectorDB()