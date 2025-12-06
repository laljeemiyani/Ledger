"""OCR Module for extracting text from images using Tesseract."""

import cv2
import pytesseract
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Dict, Any, Optional
import shutil
import sys

class OCRProcessor:
    """Handles OCR processing for image-based bank statements."""
    
    def __init__(self, image_path: str, tesseract_cmd: Optional[str] = None) -> None:
        """
        Initialize OCR processor.
        
        Args:
            image_path: Path to the image file
            tesseract_cmd: Optional path to tesseract executable
        """
        self.image_path = Path(image_path)
        
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        # Set tesseract command if provided, else attempt to find it
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            # Common paths on Windows
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                shutil.which("tesseract")
            ]
            
            found = False
            for path in common_paths:
                if path and Path(path).exists():
                    pytesseract.pytesseract.tesseract_cmd = path
                    found = True
                    break
            
            # Don't raise error yet, verify_tesseract will check when needed
    
    def verify_tesseract(self) -> bool:
        """
        Check if Tesseract is installed and accessible.
        
        Returns:
            True if available
            
        Raises:
            RuntimeError: If Tesseract is not found
        """
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            raise RuntimeError(
                "Tesseract OCR is not found. Please install it from:\n"
                "https://github.com/UB-Mannheim/tesseract/wiki"
            )
    
    def preprocess_image(self) -> np.ndarray:
        """
        Preprocess image for better OCR results.
        
        Returns:
            Processed image array
        """
        try:
            # Read image using OpenCV
            img = cv2.imread(str(self.image_path))
            if img is None:
                raise ValueError("Could not read image file")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding to binarize
            # Otsu's thresholding usually works well for documents
            _, binary = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(binary)
            
            return denoised
            
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")
    
    def extract_text(self) -> str:
        """
        Extract text from the image using OCR.
        
        Returns:
            Extracted text string
        """
        self.verify_tesseract()
        
        try:
            # Preprocess first
            processed_img = self.preprocess_image()
            
            # Convert back to PIL Image for pytesseract
            pil_img = Image.fromarray(processed_img)
            
            # Run OCR
            # --psm 6 assume a single uniform block of text
            text = pytesseract.image_to_string(pil_img, config='--psm 6')
            
            return text
            
        except Exception as e:
            raise RuntimeError(f"Error running OCR: {str(e)}")
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get image metadata.
        
        Returns:
            Dictionary with width, height, format
        """
        try:
            with Image.open(self.image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'file_path': str(self.image_path)
                }
        except Exception as e:
            raise RuntimeError(f"Error reading image metadata: {str(e)}")
