from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FileUploadResponse(BaseModel):
    document_id: int
    title: str
    filename: str
    status: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentStatusResponse(BaseModel):
    document_id: int
    title: str
    filename: str
    status: str  # processing, completed, failed
    progress: float  # 0.0 to 1.0
    current_step: Optional[str] = None
    error_message: Optional[str] = None
    chunks_processed: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

