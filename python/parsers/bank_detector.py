"""Bank Detector Module for identifying banks from statement text."""

from typing import Optional, Dict, List
import re


class BankDetector:
    """Detects bank name from statement content."""
    
    # Bank signatures: keywords and regex patterns
    SIGNATURES = {
        'HDFC': {
            'keywords': ['HDFC BANK', 'HDFC Bank', 'hdfc bank'],
            'patterns': [r'HDFC\s*BANK', r'www\.hdfcbank\.com']
        },
        'SBI': {
            'keywords': ['STATE BANK OF INDIA', 'SBI', 'sbi', 'State Bank of India'],
            'patterns': [r'State\s*Bank\s*of\s*India', r'www\.sbi\.co\.in']
        },
        'ICICI': {
            'keywords': ['ICICI BANK', 'ICICI Bank', 'icici bank'],
            'patterns': [r'ICICI\s*Bank', r'www\.icicibank\.com']
        },
        'AXIS': {
            'keywords': ['AXIS BANK', 'Axis Bank', 'axis bank'],
            'patterns': [r'AXIS\s*BANK', r'www\.axisbank\.com']
        },
        'KOTAK': {
            'keywords': ['KOTAK MAHINDRA BANK', 'Kotak Mahindra Bank', 'kotak'],
            'patterns': [r'Kotak\s*Mahindra\s*Bank', r'www\.kotak\.com']
        },
        'PNB': {
            'keywords': ['PUNJAB NATIONAL BANK', 'Punjab National Bank', 'PNB'],
            'patterns': [r'Punjab\s*National\s*Bank', r'www\.pnbindia\.in', r'pnbindia']
        },
        'BOB': {
            'keywords': ['BANK OF BARODA', 'Bank of Baroda', 'BOB'],
            'patterns': [r'Bank\s*of\s*Baroda', r'www\.bankofbaroda\.in']
        },
        'CANARA': {
            'keywords': ['CANARA BANK', 'Canara Bank'],
            'patterns': [r'Canara\s*Bank', r'www\.canarabank\.com']
        },
        'UNION': {
            'keywords': ['UNION BANK OF INDIA', 'Union Bank of India'],
            'patterns': [r'Union\s*Bank\s*of\s*India', r'www\.unionbankofindia\.co\.in']
        },
        'INDUSIND': {
            'keywords': ['INDUSIND BANK', 'IndusInd Bank'],
            'patterns': [r'IndusInd\s*Bank', r'www\.indusind\.com']
        }
    }
    
    @classmethod
    def detect(cls, text: str) -> Optional[str]:
        """
        Detect bank from text content using keywords and patterns.
        
        Args:
            text: Extracted text from bank statement
            
        Returns:
            Detected bank code (e.g., 'SBI', 'HDFC') or None
        """
        if not text:
            return None
            
        scores: Dict[str, int] = {bank: 0 for bank in cls.SIGNATURES}
        
        # Check keywords (fast)
        for bank, sig in cls.SIGNATURES.items():
            for keyword in sig['keywords']:
                if keyword in text:
                    scores[bank] += 1
        
        # Check regex patterns (if keywords aren't decisive or robust)
        for bank, sig in cls.SIGNATURES.items():
            for pattern in sig['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    scores[bank] += 2  # Higher weight for regex/exact patterns
        
        # Get bank with highest score
        best_match = max(scores.items(), key=lambda x: x[1])
        
        # Threshold: must have at least some match
        if best_match[1] > 0:
            return best_match[0]
            
        return None
    
    @classmethod
    def get_supported_banks(cls) -> List[str]:
        """Get list of supported bank codes."""
        return list(cls.SIGNATURES.keys())
