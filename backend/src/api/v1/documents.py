import logging
from uuid import UUID
from typing import List, Optional
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_active_user
from models.user import User
from models.document import Document
from services.document_service import get_document_service, DocumentService
from schemas.file import DocumentStatusResponse

router = APIRouter(prefix="/documents", tags=["Documents"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[dict])
def get_user_documents(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all documents for the current user with pagination"""
    
    document_service = get_document_service(db)
    documents = document_service.get_user_documents(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    
    return [
        {
            "id": str(doc.id),
            "filename": doc.filename,
            "title": doc.title,
            "description": doc.description,
            "file_size": doc.file_size,
            "mime_type": doc.mime_type,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
            "metadata": doc.metadata
        }
        for doc in documents
    ]


@router.get("/{document_id}")
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific document by ID"""
    
    document_service = get_document_service(db)
    document = document_service.get_document(document_id, current_user.id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {
        "id": str(document.id),
        "filename": document.filename,
        "title": document.title,
        "description": document.description,
        "file_size": document.file_size,
        "mime_type": document.mime_type,
        "file_path": document.file_path,
        "created_at": document.created_at.isoformat() if document.created_at else None,
        "updated_at": document.updated_at.isoformat() if document.updated_at else None,
        "metadata": document.metadata
    }


@router.put("/{document_id}")
def update_document(
    document_id: UUID,
    title: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a document's metadata"""
    
    document_service = get_document_service(db)
    
    updates = {}
    if title is not None:
        updates["title"] = title
    if description is not None:
        updates["description"] = description
    
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided"
        )
    
    document = document_service.update_document(
        document_id=document_id,
        user_id=current_user.id,
        **updates
    )
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {
        "id": str(document.id),
        "filename": document.filename,
        "title": document.title,
        "description": document.description,
        "updated_at": document.updated_at.isoformat() if document.updated_at else None
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a document"""
    
    document_service = get_document_service(db)
    success = document_service.delete_document(document_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document deleted successfully"}


@router.get("/search/{search_term}")
def search_documents(
    search_term: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search documents by title, filename, or description"""
    
    document_service = get_document_service(db)
    documents = document_service.search_documents(
        user_id=current_user.id,
        search_term=search_term,
        limit=limit
    )
    
    return [
        {
            "id": str(doc.id),
            "filename": doc.filename,
            "title": doc.title,
            "description": doc.description,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "metadata": doc.metadata
        }
        for doc in documents
    ]