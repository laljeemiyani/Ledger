"""Unit tests for Bank Adapters."""

import pytest
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.std_adapter import StandardAdapter
from adapters.sbi_adapter import SBIAdapter
from adapters.factory import AdapterFactory


class TestStandardAdapter:
    """Tests for StandardAdapter."""
    
    def test_process_standard_data(self):
        """Test processing standard data format."""
        df = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02'],
            'Description': ['Test 1', 'Test 2'],
            'Debit': [100.0, None],
            'Credit': [None, 200.0],
            'Balance': [1000.0, 1200.0]
        })
        
        adapter = StandardAdapter(df)
        txns = adapter.process()
        
        assert len(txns) == 2
        assert txns[0].debit == 100.0
        assert txns[0].credit == 0.0
        assert txns[1].credit == 200.0
        assert txns[0].date.year == 2024

    def test_clean_amount(self):
        """Test amount cleaning utility."""
        adapter = StandardAdapter(pd.DataFrame())
        
        assert adapter._clean_amount("1,000.50") == 1000.50
        assert adapter._clean_amount("₹ 500") == 500.0
        assert adapter._clean_amount("100 Dr") == 100.0
        assert adapter._clean_amount("200 Cr") == 200.0
        assert adapter._clean_amount(None) == 0.0


class TestSBIAdapter:
    """Tests for SBIAdapter."""
    
    def test_process_sbi_data(self):
        """Test processing pseudo-SBI data."""
        df = pd.DataFrame({
            'Txn Date': ['01-Jan-2024'],
            'Description': ['UPI Payment'],
            'Ref No./Cheque No.': ['REF123'],
            'Debit': [500.0],
            'Credit': [0.0],
            'Balance': [5000.0]
        })
        
        adapter = SBIAdapter(df)
        txns = adapter.process()
        
        assert len(txns) == 1
        assert txns[0].reference_no == 'REF123'
        assert txns[0].description == 'UPI Payment'


class TestAdapterFactory:
    """Tests for AdapterFactory."""
    
    def test_get_sbi_adapter(self):
        df = pd.DataFrame()
        adapter = AdapterFactory.get_adapter('SBI', df)
        assert isinstance(adapter, SBIAdapter)
        
    def test_get_default_adapter(self):
        df = pd.DataFrame()
        adapter = AdapterFactory.get_adapter('UNKNOWN', df)
        assert isinstance(adapter, StandardAdapter)
