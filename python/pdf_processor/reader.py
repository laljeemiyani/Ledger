"""PDF Reader Module for processing bank statements."""

from typing import Optional, Dict, Any
from pathlib import Path
import PyPDF2


class PDFReader:
    """Handles reading and parsing PDF files."""
    
    def __init__(self, pdf_path: str, password: Optional[str] = None) -> None:
        """
        Initialize PDF reader.
        
        Args:
            pdf_path: Path to the PDF file
            password: Optional password for encrypted PDFs
        """
        self.pdf_path = Path(pdf_path)
        self.password = password
        self._pdf_reader: Optional[PyPDF2.PdfReader] = None
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    def is_encrypted(self) -> bool:
        """
        Check if PDF is password protected.
        
        Returns:
            True if PDF is encrypted, False otherwise
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return reader.is_encrypted
        except Exception as e:
            raise RuntimeError(f"Error checking PDF encryption: {str(e)}")
    
    def unlock(self, password: str) -> bool:
        """
        Attempt to unlock encrypted PDF.
        
        Args:
            password: Password to try
            
        Returns:
            True if unlock successful, False otherwise
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.is_encrypted:
                    result = reader.decrypt(password)
                    if result == 1:  # Password correct
                        self.password = password
                        return True
                    return False
                return True  # Not encrypted
        except Exception as e:
            raise RuntimeError(f"Error unlocking PDF: {str(e)}")
    
    def read(self) -> Dict[str, Any]:
        """
        Read PDF content and metadata.
        
        Returns:
            Dictionary containing:
                - num_pages: Number of pages
                - text: Extracted text from all pages
                - metadata: PDF metadata (author, title, etc.)
                - is_encrypted: Whether PDF was encrypted
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Handle encryption
                is_encrypted = reader.is_encrypted
                if is_encrypted:
                    if not self.password:
                        raise ValueError("PDF is encrypted but no password provided")
                    if reader.decrypt(self.password) != 1:
                        raise ValueError("Invalid password for encrypted PDF")
                
                # Extract metadata
                metadata = {}
                if reader.metadata:
                    metadata = {
                        'author': reader.metadata.get('/Author', ''),
                        'title': reader.metadata.get('/Title', ''),
                        'subject': reader.metadata.get('/Subject', ''),
                        'creator': reader.metadata.get('/Creator', ''),
                        'producer': reader.metadata.get('/Producer', ''),
                        'creation_date': reader.metadata.get('/CreationDate', ''),
                    }
                
                # Extract text from all pages
                num_pages = len(reader.pages)
                text_content = []
                
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    text_content.append(text)
                
                return {
                    'num_pages': num_pages,
                    'text': '\n\n'.join(text_content),
                    'metadata': metadata,
                    'is_encrypted': is_encrypted,
                    'file_path': str(self.pdf_path),
                }
                
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {str(e)}")
    
    def get_page_text(self, page_number: int) -> str:
        """
        Extract text from a specific page.
        
        Args:
            page_number: Page number (0-indexed)
            
        Returns:
            Extracted text from the page
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if reader.is_encrypted and self.password:
                    reader.decrypt(self.password)
                
                if page_number < 0 or page_number >= len(reader.pages):
                    raise ValueError(f"Invalid page number: {page_number}")
                
                page = reader.pages[page_number]
                return page.extract_text()
                
        except Exception as e:
            raise RuntimeError(f"Error extracting page text: {str(e)}")
