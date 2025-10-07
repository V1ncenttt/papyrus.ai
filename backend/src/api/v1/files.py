import logging
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, File, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import uuid

from schemas.file import FileUploadResponse, DocumentStatusResponse
from core.config import settings
from core.dependencies import get_current_active_user
from models.user import User
from services.storage_service import get_storage
from services.pdf_processor import PDFProcessor
from services.vectordb_service import VectorDBInterface, ChromaVectorDB, DocumentChunk
from services.document_service import get_document_service, DocumentService
from models.document import Document

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

router = APIRouter(prefix="/files", tags=["Files"])

# Configure logger for this module
logger = logging.getLogger(__name__)


def validate_pdf_structure(file_content: bytes) -> bool:
    return True  # TODO: implement actual PDF structure validation

def scan_pdf_content(file_content: bytes) -> bool:
    return True  # TODO: implement actual PDF content scanning
from functools import lru_cache

@lru_cache()
def get_pdf_processor() -> PDFProcessor:
    """Create singleton PDFProcessor via dependency injection"""
    return PDFProcessor()

@lru_cache()
def get_vector_db() -> VectorDBInterface:
    return ChromaVectorDB()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    pdf_processor: PDFProcessor = Depends(get_pdf_processor),  # Reuses same instance
    vector_db: VectorDBInterface = Depends(get_vector_db),  # Reuses same instance
    current_user: User = Depends(get_current_active_user),
):
    """
    Endpoint to handle file uploads.
    """
    # TODO: decide how to deal with images
    
    
    
    logger.info("Starting file upload")
    logger.info(f"Starting upload for user {current_user.id}")
    logger.info(f"File: {file.filename}, Size: {file.size}, Content-Type: {file.content_type}")
    
    # 1: get file  from request
    file_content = await file.read()
    logger.info(f"Read {len(file_content)} bytes from file")

    # 2: validate file type and size
    if file.content_type != "application/pdf":
        logger.error("Invalid file type")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    if len(file_content) < 100:  # Too small to be valid PDF
        raise HTTPException(status_code=400, detail="File too small")
    
    # 3. Validate PDF structure
    if not validate_pdf_structure(file_content):
        raise HTTPException(status_code=400, detail="Invalid or corrupted PDF")
    

    # 4. Scan for malicious content
    if not scan_pdf_content(file_content):
        raise HTTPException(status_code=400, detail="PDF contains suspicious content")
    
    # 5. Save file to storage with a secure filename
    logger.info("Saving file to storage")
    file_uuid = str(uuid.uuid4())
    secure_filename = f"{file_uuid}.pdf"
    storage = get_storage()
    file_path = await storage.save_file(file_content, secure_filename)
    logger.info(f"File saved to storage at {file_path}")

    # 6: extract bib metadata using pdf2bib and if not found use filename as title
    logger.info("Extracting bibliographic metadata from PDF")
    bib_metadata = await pdf_processor.extract_bib_metadata(file_path)
    logger.info(f"Extracted metadata: {bib_metadata}")
    if not bib_metadata:
        bib_metadata = {"title": secure_filename}
    logger.info("Processing PDF to extract markdown text")

    # 6: use mistral api to get .md file
    markdown_text = await pdf_processor.process_pdf(file_content, secure_filename)
    
    # 5: add .md file to vector db
    logger.info("Adding document to vector database")
    await vector_db.add_document(
        document_id=file_uuid,
        content=markdown_text,
        metadata={
            "user_id": current_user.id,
            "filename": file.filename,
            "document_title": bib_metadata.get("title", file.filename)
        }
    )
    
    # 6: add info to sql db
    logger.info("Saving document info to database")
    try:
        document_service = get_document_service(db)
        document = document_service.create_document(
            filename=file.filename,
            file_path=file_path,
            user_id=current_user.id,
            title=bib_metadata.get("title", file.filename)
        )
        logger.info(f"Document saved to database with ID: {document.id}")
    except Exception as e:
        logger.error(f"Failed to save document to database: {str(e)}")
        # Continue even if database save fails, as the file and vector db are already processed
    

    logger.info(f"Upload completed for user {current_user.id}")
    
    return {
        "message": "Upload completed", 
        "user_id": current_user.id,
        "document_id": document.id if 'document' in locals() else None,
        "filename": file.filename,
        "title": bib_metadata.get("title", file.filename)
    }
@router.get("/upload/{document_id}/status")
async def get_upload_status(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get the status of a file upload/processing task.
    """
    # TODO: Query document from database
    # TODO: Check if document belongs to current user
    # TODO: Return status, progress, and metadata
    
    return {
        "document_id": document_id,
        "status": "processing",  # processing, completed, failed
        "progress": 0.5,  # 0.0 to 1.0
        "message": "Extracting text from PDF...",
        "created_at": "2024-10-02T10:30:00Z",
        "updated_at": "2024-10-02T10:30:30Z"
    }