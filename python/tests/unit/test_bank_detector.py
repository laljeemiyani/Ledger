"""Unit tests for Bank Detector module."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from parsers.bank_detector import BankDetector


class TestBankDetector:
    """Test cases for BankDetector class."""
    
    def test_detect_hdfc(self):
        """Test detecting HDFC bank."""
        text = "Account Statement for HDFC Bank Account No: 123456"
        assert BankDetector.detect(text) == 'HDFC'
    
    def test_detect_sbi(self,):
        """Test detecting SBI bank."""
        text = "STATE BANK OF INDIA Statement Date: 01-01-2024"
        assert BankDetector.detect(text) == 'SBI'
    
    def test_detect_icici(self):
        """Test detecting ICICI bank."""
        text = "Welcome to ICICI Bank Internet Banking"
        assert BankDetector.detect(text) == 'ICICI'
    
    def test_detect_regex_pattern(self):
        """Test detecting via regex pattern."""
        text = "Visit us at www.axisbank.com"
        assert BankDetector.detect(text) == 'AXIS'
        
    def test_ambiguous_text(self):
        """Test ambiguous text chooses highest score."""
        # Mentions HDFC but header says SBI clearly
        text = "STATE BANK OF INDIA. Transfer to HDFC."
        # SBI pattern matches 'State Bank of India' (score via keyword+regex likely high)
        # HDFC won't match because 'HDFC' alone isn't in keywords (only HDFC Bank)
        assert BankDetector.detect(text) == 'SBI'
        
    def test_no_match(self):
        """Test text with no bank info."""
        text = "Random statement text with no bank name"
        assert BankDetector.detect(text) is None
    
    def test_empty_text(self):
        """Test empty text."""
        assert BankDetector.detect("") is None
    
    def test_supported_banks(self):
        """Test getting supported banks."""
        banks = BankDetector.get_supported_banks()
        assert 'HDFC' in banks
        assert 'SBI' in banks
        assert len(banks) >= 10
