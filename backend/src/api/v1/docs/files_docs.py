upload_file_docs = {
    "summary": "Upload PDF Document",
    "description": """
    Upload a PDF document for processing and analysis. The endpoint will:
    - Validate the PDF file (type, size, structure)
    - Extract bibliographic metadata using pdf2bib
    - Convert PDF content to markdown using Mistral API
    - Store the document in vector database for semantic search
    - Save document metadata to SQL database
    
    Maximum file size: 50MB
    Supported formats: PDF only
    """,
    "responses": {
        201: {
            "description": "File uploaded and processed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Upload completed",
                        "user_id": 1,
                        "document_id": 123,
                        "filename": "research_paper.pdf",
                        "title": "Machine Learning in Healthcare: A Comprehensive Review"
                    }
                }
            }
        },
        400: {
            "description": "Invalid file or request",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_file_type": {
                            "summary": "Invalid file type",
                            "value": {"detail": "Only PDF files are supported"}
                        },
                        "file_too_small": {
                            "summary": "File too small",
                            "value": {"detail": "File too small"}
                        },
                        "corrupted_pdf": {
                            "summary": "Corrupted PDF",
                            "value": {"detail": "Invalid or corrupted PDF"}
                        },
                        "suspicious_content": {
                            "summary": "Suspicious content",
                            "value": {"detail": "PDF contains suspicious content"}
                        }
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        },
        413: {
            "description": "File too large",
            "content": {
                "application/json": {
                    "example": {"detail": "File too large"}
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "file"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal server error during processing",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to process document"}
                }
            }
        }
    }
}

get_upload_status_docs = {
    "summary": "Get Document Upload Status",
    "description": """
    Retrieve the current status of a document upload and processing task.
    This endpoint provides real-time information about the document processing pipeline.
    
    Status values:
    - "processing": Document is being processed
    - "completed": Processing finished successfully  
    - "failed": Processing failed with error
    - "pending": Document queued for processing
    """,
    "responses": {
        200: {
            "description": "Upload status retrieved successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "processing": {
                            "summary": "Document being processed",
                            "value": {
                                "document_id": 123,
                                "status": "processing",
                                "progress": 0.5,
                                "message": "Extracting text from PDF...",
                                "created_at": "2024-10-02T10:30:00Z",
                                "updated_at": "2024-10-02T10:30:30Z"
                            }
                        },
                        "completed": {
                            "summary": "Document processing completed",
                            "value": {
                                "document_id": 123,
                                "status": "completed",
                                "progress": 1.0,
                                "message": "Document processed successfully",
                                "created_at": "2024-10-02T10:30:00Z",
                                "updated_at": "2024-10-02T10:32:15Z"
                            }
                        },
                        "failed": {
                            "summary": "Document processing failed",
                            "value": {
                                "document_id": 123,
                                "status": "failed",
                                "progress": 0.3,
                                "message": "Failed to extract text from PDF",
                                "created_at": "2024-10-02T10:30:00Z",
                                "updated_at": "2024-10-02T10:31:45Z"
                            }
                        }
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        },
        403: {
            "description": "Access forbidden - document doesn't belong to user",
            "content": {
                "application/json": {
                    "example": {"detail": "Access denied to this document"}
                }
            }
        },
        404: {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Document not found"}
                }
            }
        }
    }
}