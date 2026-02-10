"""ChromaDB retrieval service for DSM-5 vector search"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional

from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RetrievalService:
    """Manages ChromaDB collection and performs similarity search"""

    def __init__(self):
        self._client = None
        self._collection = None

    @property
    def client(self) -> chromadb.ClientAPI:
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            logger.info(f"ChromaDB client initialized at {settings.chroma_persist_dir}")
        return self._client

    @property
    def collection(self) -> chromadb.Collection:
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=settings.chroma_collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(
                f"ChromaDB collection '{settings.chroma_collection_name}' loaded "
                f"with {self._collection.count()} documents"
            )
        return self._collection

    def query(
        self,
        query_embedding: List[float],
        top_k: int = None,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Query the collection by embedding vector.
        Returns documents, metadatas, distances, and ids.
        """
        k = top_k or settings.retrieval_top_k
        doc_count = self.collection.count()

        if doc_count == 0:
            logger.warning("ChromaDB collection is empty — no documents to search")
            return {"documents": [], "metadatas": [], "distances": [], "ids": []}

        # Clamp k to available document count
        k = min(k, doc_count)

        query_params = {
            "query_embeddings": [query_embedding],
            "n_results": k,
        }
        if where:
            query_params["where"] = where
        if where_document:
            query_params["where_document"] = where_document

        results = self.collection.query(**query_params)

        # Flatten from batch format (single query)
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "ids": results["ids"][0] if results["ids"] else [],
        }

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the current collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": settings.chroma_collection_name,
                "document_count": count,
                "persist_directory": settings.chroma_persist_dir,
                "status": "ready" if count > 0 else "empty",
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {
                "collection_name": settings.chroma_collection_name,
                "document_count": 0,
                "persist_directory": settings.chroma_persist_dir,
                "status": "error",
                "error": str(e),
            }

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
    ):
        """Add documents to the collection"""
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        logger.info(f"Added {len(ids)} documents to collection")

    def delete_collection(self):
        """Delete the entire collection for re-ingestion"""
        try:
            self.client.delete_collection(settings.chroma_collection_name)
            self._collection = None
            logger.info(f"Deleted collection '{settings.chroma_collection_name}'")
        except Exception as e:
            logger.warning(f"Could not delete collection: {e}")

    def is_ready(self) -> bool:
        """Check if the collection exists and has documents"""
        try:
            return self.collection.count() > 0
        except Exception:
            return False
