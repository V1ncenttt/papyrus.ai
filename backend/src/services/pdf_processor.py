from mistralai import Mistral
from core.config import settings
import logging
import json
import pdf2bib
import asyncio

logger = logging.getLogger(__name__)
pdf2bib.config.set('verbose',False)

class PDFProcessor:
    def __init__(self):
        self.mistral_client = Mistral(api_key=settings.mistral_api_key)
    
    async def process_pdf(self, file_content: bytes, file_name: str) -> str:
        """
        Process the PDF file content and return extracted markdown text.
        """
        # TODO : handle retry l;ogic and rate limiting + error handling
        uploaded_file = await self.mistral_client.files.upload_async(
            file = {
                'file_name': file_name,
                'content': file_content,
            },
            purpose= 'ocr'
        )
        logger.info(f"Uploaded file to Mistral with ID: {uploaded_file.id}")
        pdf_response = await self.mistral_client.ocr.process_async(
            document={
                "type": "file",
                "file_id": uploaded_file.id,
            },
            model="mistral-ocr-latest",
            include_image_base64=True
        )

        # Process the response
        response_dict = json.loads(pdf_response.model_dump_json())
        
        # Extract only markdown content (no images)
        return self._extract_markdown_content(response_dict)
    
    def _extract_markdown_content(self, response_dict: dict) -> str:
        """
        Private method to extract markdown content from Mistral OCR response.
        Images are ignored for vector database storage.
        """
        # TODO: decide how to deal with images
        markdown_content = ""
        
        # Process pages
        for page in response_dict.get("pages", []):
            # Add page markdown content
            if page.get("markdown"):
                markdown_content += page["markdown"] + "\n\n"
        
        return markdown_content.strip()

    async def extract_bib_metadata(self, file_path: str) -> dict:
        """
        Extract bibliographic metadata from the PDF file content.
        """
        # TODO : handle cases where pdf2bib fails because the file is not a paper
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, pdf2bib.pdf2bib, file_path)
        
        title = result["metadata"]["title"]
        summary = result['validation_info']["summary"]
        bibtex = result["bibtex"]
        authors = result["metadata"]["author"]

        return {
            "title": title, 
            "summary": summary,
            "bibtex": bibtex,
            "authors": authors
        }

