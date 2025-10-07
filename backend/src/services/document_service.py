from uuid import UUID
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from models.document import Document

class DocumentService:
    """Service for handling document CRUD operations"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create_document(
        self, 
        filename: str, 
        file_path: str, 
        user_id: UUID,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Document:
        """Create a new document record in the database"""
        
        document = Document(
            filename=filename,
            file_path=file_path,
            user_id=user_id,
            title=title or filename,
            metadata=metadata or {}
        )
        
        self.db_session.add(document)
        self.db_session.commit()
        self.db_session.refresh(document)
        
        return document
    
    def get_document(self, document_id: UUID, user_id: UUID) -> Optional[Document]:
        """Get a document by ID for a specific user"""
        
        return self.db_session.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()
    
    def get_user_documents(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[Document]:
        """Get all documents for a specific user with pagination"""
        
        return (
            self.db_session.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def update_document(
        self, 
        document_id: UUID, 
        user_id: UUID,
        **updates
    ) -> Optional[Document]:
        """Update a document record"""
        
        # First verify the document belongs to the user
        document = self.get_document(document_id, user_id)
        if not document:
            return None
        
        # Update the document
        for key, value in updates.items():
            if hasattr(document, key):
                setattr(document, key, value)
        
        self.db_session.commit()
        
        # Return updated document
        return document
    
    def delete_document(self, document_id: UUID, user_id: UUID) -> bool:
        """Delete a document record"""
        
        document = self.get_document(document_id, user_id)
        if not document:
            return False
        
        self.db_session.delete(document)
        self.db_session.commit()
        
        return True
    
    def search_documents(
        self, 
        user_id: UUID, 
        search_term: str,
        limit: int = 50
    ) -> List[Document]:
        """Search documents by title or filename"""
        
        from sqlalchemy import or_
        
        return (
            self.db_session.query(Document)
            .filter(
                Document.user_id == user_id,
                or_(
                    Document.title.ilike(f"%{search_term}%"),
                    Document.filename.ilike(f"%{search_term}%")
                )
            )
            .order_by(Document.created_at.desc())
            .limit(limit)
            .all()
        )


def get_document_service(db_session: Session) -> DocumentService:
    """Factory function to create DocumentService instance"""
    return DocumentService(db_session)
from typing import List, Dict, Any, Optional
from dataclasses import dataclass