"""Integration tests for the full data processing pipeline."""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from parsers.csv_parser import CSVParser
from parsers.excel_parser import ExcelParser
from parsers.bank_detector import BankDetector
from adapters.factory import AdapterFactory
from adapters.base import Transaction


class TestPipeline:
    """Integration checks for data flow."""
    
    def test_csv_to_adapter_flow(self, tmp_path):
        """Test flow from CSV file to standardized transactions."""
        # 1. Create CSV
        csv_path = tmp_path / "statement.csv"
        csv_path.write_text(
            "Txn Date,Description,Debit,Credit,Balance\n"
            "01-Jan-2024,Payment to Vendor,500.00,,1000.00\n"
            "02-Jan-2024,Salary,,2000.00,3000.00"
        )
        
        # 2. Parse CSV
        parser = CSVParser(str(csv_path))
        df = parser.parse()
        
        # 3. Detect Bank (Simulated based on content or metadata)
        # Using BankDetector directly on dummy text for integration check
        bank_name = BankDetector.detect("Welcome to SBI Banking") # Simulating detected bank
        
        # 4. Get Adapter
        adapter = AdapterFactory.get_adapter(bank_name, df)
        
        # 5. Process
        transactions = adapter.process()
        
        # 6. Verify
        assert len(transactions) == 2
        assert transactions[0].debit == 500.0
        assert transactions[1].credit == 2000.0
        assert isinstance(transactions[0], Transaction)
        assert adapter.__class__.__name__ == 'SBIAdapter' # Should be SBI if detected

    def test_generic_pipeline(self, tmp_path):
        """Test flow for unknown bank (Generic path)."""
        csv_path = tmp_path / "unknown.csv"
        csv_path.write_text(
            "Date,Description,Amount\n"
            "2024-01-01,Test,-100\n"
            "2024-01-02,Test2,200"
        )
        
        parser = CSVParser(str(csv_path))
        df = parser.parse()
        
        # No bank detected
        bank_name = BankDetector.detect("Generic statement") # Returns None
        
        adapter = AdapterFactory.get_adapter(bank_name or "", df)
        transactions = adapter.process()
        
        assert len(transactions) == 2
        assert adapter.__class__.__name__ == 'StandardAdapter'
        assert transactions[0].debit == 100.0 # Negative amount handled as debit
