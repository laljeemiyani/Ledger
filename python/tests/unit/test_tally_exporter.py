"""Unit tests for Tally XML Exporter."""

import pytest
from datetime import datetime
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.base import Transaction
from exporters.tally_xml import TallyXMLExporter


class TestTallyXMLExporter:
    """Test cases for Tally XML generation."""
    
    def test_generate_payment_xml(self):
        """Test generating XML for a payment transaction."""
        txn = Transaction(
            date=datetime(2024, 1, 1),
            description="Payment to Vendor",
            debit=500.0,
            credit=0.0,
            balance=1000.0,
            reference_no="REF001"
        )
        
        exporter = TallyXMLExporter([txn])
        xml_str = exporter.generate_xml()
        
        # Verify structure
        root = ET.fromstring(xml_str)
        voucher = root.find(".//VOUCHER")
        assert voucher is not None
        assert voucher.get("VCHTYPE") == "Payment"
        
        date = voucher.find("DATE").text
        assert date == "20240101"
        
        narr = voucher.find("NARRATION").text
        assert narr == "Payment to Vendor"
        
        # Check amounts
        entries = voucher.findall(".//ALLLEDGERENTRIES.LIST")
        assert len(entries) == 2
        
        # Entry 1: Bank (Credit -500)
        bank_entry = entries[0]
        assert bank_entry.find("LEDGERNAME").text == "Bank Account"
        assert bank_entry.find("AMOUNT").text == "-500.00"
        
        # Entry 2: Suspense (Debit 500)
        suspense_entry = entries[1]
        assert suspense_entry.find("LEDGERNAME").text == "Suspense Account"
        assert suspense_entry.find("AMOUNT").text == "500.00"

    def test_generate_receipt_xml(self):
        """Test generating XML for a receipt transaction."""
        txn = Transaction(
            date=datetime(2024, 1, 2),
            description="Salary Received",
            debit=0.0,
            credit=2000.0,
            balance=3000.0
        )
        
        exporter = TallyXMLExporter([txn])
        xml_str = exporter.generate_xml()
        
        root = ET.fromstring(xml_str)
        voucher = root.find(".//VOUCHER")
        assert voucher.get("VCHTYPE") == "Receipt"
        
        entries = voucher.findall(".//ALLLEDGERENTRIES.LIST")
        
        # Entry 1: Bank (Debit 2000)
        bank_entry = entries[0]
        assert bank_entry.find("LEDGERNAME").text == "Bank Account"
        assert bank_entry.find("AMOUNT").text == "2000.00"

    def test_multiple_transactions(self):
        """Test generating XML for multiple transactions."""
        txns = [
            Transaction(datetime(2024, 1, 1), "T1", 100, 0, 100),
            Transaction(datetime(2024, 1, 2), "T2", 0, 200, 300)
        ]
        
        exporter = TallyXMLExporter(txns)
        xml_str = exporter.generate_xml()
        
        root = ET.fromstring(xml_str)
        vouchers = root.findall(".//VOUCHER")
        assert len(vouchers) == 2
        assert vouchers[0].get("VCHTYPE") == "Payment"
        assert vouchers[1].get("VCHTYPE") == "Receipt"
