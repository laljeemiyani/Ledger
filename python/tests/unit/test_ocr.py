"""Unit tests for OCR Processor module."""

import pytest
from pathlib import Path
import sys
import numpy as np
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from image_processor.ocr import OCRProcessor


class TestOCRProcessor:
    """Test cases for OCRProcessor class."""
    
    @pytest.fixture
    def mock_cv2(self):
        """Mock cv2 module."""
        with patch('image_processor.ocr.cv2') as mock:
            # Mock imread to return a dummy image array
            mock.imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
            # Mock cvtColor
            mock.cvtColor.return_value = np.zeros((100, 100), dtype=np.uint8)
            # Mock threshold
            mock.threshold.return_value = (127, np.zeros((100, 100), dtype=np.uint8))
            # Mock denoising
            mock.fastNlMeansDenoising.return_value = np.zeros((100, 100), dtype=np.uint8)
            # Mock constants
            mock.COLOR_BGR2GRAY = 6
            mock.THRESH_BINARY = 0
            mock.THRESH_OTSU = 8
            yield mock
            
    @pytest.fixture
    def mock_pytesseract(self):
        """Mock pytesseract module."""
        with patch('image_processor.ocr.pytesseract') as mock:
            mock.get_tesseract_version.return_value = '5.0.0'
            mock.image_to_string.return_value = "Extracted Text"
            yield mock
            
    @pytest.fixture
    def sample_image(self, tmp_path):
        """Create a dummy image file path."""
        img_path = tmp_path / "test.png"
        img_path.write_bytes(b'fake image content')
        return img_path
    
    def test_invalid_file_path(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with pytest.raises(FileNotFoundError):
            processor = OCRProcessor('nonexistent.png')
            
    def test_initialization(self, sample_image):
        """Test OCRProcessor initialization."""
        processor = OCRProcessor(str(sample_image))
        assert processor.image_path == sample_image
        
    def test_verify_tesseract_success(self, sample_image, mock_pytesseract):
        """Test verifying tesseract availability."""
        processor = OCRProcessor(str(sample_image))
        assert processor.verify_tesseract() is True
        
    def test_verify_tesseract_failure(self, sample_image):
        """Test verify fails when tesseract missing."""
        with patch('image_processor.ocr.pytesseract.get_tesseract_version', side_effect=Exception("Not found")):
            processor = OCRProcessor(str(sample_image))
            with pytest.raises(RuntimeError, match="Tesseract OCR is not found"):
                processor.verify_tesseract()
                
    def test_extract_text(self, sample_image, mock_cv2, mock_pytesseract):
        """Test full text extraction flow."""
        processor = OCRProcessor(str(sample_image))
        
        # Patch PIL.Image.fromarray since we are using fake arrays (or real dependencies if installed)
        # We can rely on real PIL usually, but cv2 is mocked to return numpy arrays
        # so PIL.Image.fromarray needs a valid numpy array. our mock_cv2 returns that.
        
        text = processor.extract_text()
        assert text == "Extracted Text"
        mock_pytesseract.image_to_string.assert_called_once()
    
    def test_preprocess_image(self, sample_image, mock_cv2):
        """Test image preprocessing."""
        processor = OCRProcessor(str(sample_image))
        result = processor.preprocess_image()
        
        assert isinstance(result, np.ndarray)
        mock_cv2.imread.assert_called_with(str(sample_image))
        mock_cv2.cvtColor.assert_called()
        mock_cv2.threshold.assert_called()

    def test_get_metadata(self, sample_image):
        """Test getting image metadata."""
        # We need to mock PIL.Image.open for this since file is fake bytes
        with patch('PIL.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_img.__enter__.return_value = mock_img
            mock_img.width = 100
            mock_img.height = 200
            mock_img.format = 'PNG'
            mock_img.mode = 'RGB'
            mock_open.return_value = mock_img
            
            processor = OCRProcessor(str(sample_image))
            meta = processor.get_metadata()
            
            assert meta['width'] == 100
            assert meta['height'] == 200
            assert meta['format'] == 'PNG'
