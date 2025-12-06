"""Unit tests for PDF Reader module."""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pdf_processor.reader import PDFReader


class TestPDFReader:
    """Test cases for PDFReader class."""
    
    def test_invalid_file_path(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with pytest.raises(FileNotFoundError):
            reader = PDFReader('nonexistent.pdf')
    
    def test_pdf_reader_initialization(self, tmp_path):
        """Test PDFReader can be initialized with valid path."""
        # Create a temporary empty file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("")
        
        # This will fail when trying to read, but init should work
        reader = PDFReader(str(pdf_file))
        assert reader.pdf_path == pdf_file
        assert reader.password is None
    
    def test_password_parameter(self, tmp_path):
        """Test PDFReader stores password parameter."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("")
        
        reader = PDFReader(str(pdf_file), password="test123")
        assert reader.password == "test123"


# Note: Additional tests require sample PDF files
# These will be added in integration tests with actual bank statement PDFs
