import logging

import chromadb
from chromadb.config import Settings as ChromaSettings
from config import settings

logger = logging.getLogger(__name__)


class VectorDatabase:
    """ChromaDB client wrapper"""

    def __init__(self):
        self.client = None
        self.collection = None

    def connect(self):
        """Initialize ChromaDB client"""
        try:
            # Create ChromaDB client
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port,
                settings=ChromaSettings(
                    chroma_server_host=settings.chroma_host,
                    chroma_server_http_port=settings.chroma_port,
                ),
            )

            # Get or create collection for papers
            self.collection = self.client.get_or_create_collection(
                name="papers",
                metadata={"description": "Research papers and their embeddings"},
            )

            logger.info("Connected to ChromaDB successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {str(e)}")
            return False

    def add_documents(self, documents, embeddings, metadatas, ids):
        """Add documents to the collection"""
        if not self.collection:
            raise RuntimeError("Vector database not connected. Call connect() first.")

        try:
            self.collection.add(
                documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids
            )
            logger.info(f"Added {len(documents)} documents to ChromaDB")

        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {str(e)}")
            raise

    def search(self, query_embeddings, n_results=10, where=None):
        """Search for similar documents"""
        if not self.collection:
            raise RuntimeError("Vector database not connected. Call connect() first.")

        try:
            results = self.collection.query(
                query_embeddings=query_embeddings, n_results=n_results, where=where
            )
            return results

        except Exception as e:
            logger.error(f"Failed to search ChromaDB: {str(e)}")
            raise

    def delete_documents(self, ids):
        """Delete documents by IDs"""
        if not self.collection:
            raise RuntimeError("Vector database not connected. Call connect() first.")

        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from ChromaDB")

        except Exception as e:
            logger.error(f"Failed to delete documents from ChromaDB: {str(e)}")
            raise

    def check_connection(self):
        """Check ChromaDB connection health"""
        try:
            if self.client:
                # Try to list collections to verify connection
                self.client.list_collections()
                return True
            return False

        except Exception as e:
            logger.error(f"ChromaDB health check failed: {str(e)}")
            return False

    def close(self):
        """Close ChromaDB connection"""
        try:
            if self.client:
                # ChromaDB client doesn't have explicit close method
                self.client = None
                self.collection = None
                logger.info("ChromaDB connection closed")

        except Exception as e:
            logger.error(f"Error closing ChromaDB connection: {str(e)}")


# Global vector database instance
vector_db = VectorDatabase()
