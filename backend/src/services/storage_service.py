from abc import ABC, abstractmethod
from typing import BinaryIO
import boto3
import os
from pathlib import Path
import uuid
from core.config import settings

class StorageInterface(ABC):
    """Abstract storage interface"""
    
    @abstractmethod
    async def save_file(self, file_content: bytes, filename: str) -> str:
        """Save file and return the file path/URL"""
        pass
    
    @abstractmethod
    async def get_file(self, file_path: str) -> bytes:
        """Retrieve file content"""
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete file"""
        pass

class LocalStorage(StorageInterface):
    """Local file system storage for development"""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
    
    async def save_file(self, file_content: bytes, filename: str) -> str:
        file_path = self.upload_dir / filename
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return str(file_path)
    
    async def get_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            return f.read()
    
    async def delete_file(self, file_path: str) -> bool:
        try:
            os.remove(file_path)
            return True
        except OSError:
            return False

class S3Storage(StorageInterface):
    """AWS S3 storage for production"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.s3_bucket_name
    
    async def save_file(self, file_content: bytes, filename: str) -> str:
        """Upload to S3 and return S3 key"""
        s3_key = f"documents/{filename}"
        
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=file_content,
            ContentType='application/pdf'
        )
        
        return s3_key  # Return S3 key as path
    
    async def get_file(self, file_path: str) -> bytes:
        """Download from S3"""
        response = self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=file_path
        )
        return response['Body'].read()
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except Exception:
            return False

# Storage factory
def get_storage() -> StorageInterface:
    """Return storage implementation based on configuration"""
    if settings.storage_provider == "s3":
        return S3Storage()
    else:
        return LocalStorage(settings.local_upload_dir)