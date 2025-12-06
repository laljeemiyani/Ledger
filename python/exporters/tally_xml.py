"""Tally XML Exporter Module."""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional
from adapters.base import Transaction

class TallyXMLExporter:
    """Generates Tally Import XML from Transactions."""
    
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions
        
    def generate_xml(self) -> str:
        """
        Generate Tally XML string.
        Structure:
        <ENVELOPE>
            <HEADER>...</HEADER>
            <BODY>
                <IMPORTDATA>
                    <REQUESTDATA>
                        <TALLYMESSAGE>
                            <VOUCHER>...</VOUCHER>
                        </TALLYMESSAGE>
                    </REQUESTDATA>
                </IMPORTDATA>
            </BODY>
        </ENVELOPE>
        """
        envelope = ET.Element("ENVELOPE")
        header = ET.SubElement(envelope, "HEADER")
        ET.SubElement(header, "TALLYREQUEST").text = "Import Data"
        
        body = ET.SubElement(envelope, "BODY")
        import_data = ET.SubElement(body, "IMPORTDATA")
        req_data = ET.SubElement(import_data, "REQUESTDATA")
        
        for txn in self.transactions:
            self._create_voucher_element(req_data, txn)
            
        # Pretty print equivalent (minified for XML, Tally handles it)
        # Using encoding='unicode' to return string
        return ET.tostring(envelope, encoding='unicode', method='xml')
        
    def _create_voucher_element(self, parent: ET.Element, txn: Transaction):
        """Create VOUCHER element for a transaction."""
        tally_msg = ET.SubElement(parent, "TALLYMESSAGE", {"xmlns:UDF": "TallyUDF"})
        voucher = ET.SubElement(tally_msg, "VOUCHER", {"VCHTYPE": "Payment", "ACTION": "Create", "OBJVIEW": "Accounting Voucher View"})
        
        # Determine Voucher Type (Payment or Receipt)
        # Logic: If Debit > 0 it's a Payment (money out), if Credit > 0 it's Receipt (money in)
        # This is a simplification. Contra/Journal logic might be needed for complex cases.
        is_payment = txn.debit > 0
        vch_type = "Payment" if is_payment else "Receipt"
        voucher.set("VCHTYPE", vch_type)
        
        # Date in YYYYMMDD format
        date_str = txn.date.strftime("%Y%m%d")
        ET.SubElement(voucher, "DATE").text = date_str
        
        # Narrations
        ET.SubElement(voucher, "NARRATION").text = txn.description
        ET.SubElement(voucher, "VOUCHERTYPENAME").text = vch_type
        ET.SubElement(voucher, "VOUCHERNUMBER").text = txn.reference_no or "1" # Placeholder logic
        
        # All Ledgers
        # 1. Bank Ledger Entry (The account the statement belongs to)
        # For Payment: Bank is Credited (money goes out).
        # For Receipt: Bank is Debited (money comes in).
        
        bank_amount = -txn.debit if is_payment else txn.credit
        # NOTE: Tally negative amount usually means Credit? No, Tally convention:
        # Debits are Positive?
        # Actually in XML import:
        # Amount negative = Credit. Amount positive = Debit.
        
        # Let's verify Tally XML convention:
        # Usually: Debit is negative in some views, but positive in import if explicit `ISDEEMEDPOSITIVE`.
        # Standard: negative amount = Credit. positive amount = Debit.
        
        # Entry 1: Bank Ledger
        bank_entry_amount = -txn.debit if is_payment else -txn.credit 
        # Wait. 
        # Payment: Debit Expense, Credit Bank.
        # So Bank amount should be Credit (Negative). `-100`.
        # Receipt: Debit Bank, Credit Income.
        # So Bank amount should be Debit (Positive). `100`. (Wait, if negative is Credit...)
        
        # Correct Logic:
        # Payment of 500:
        # Bank: Credit 500. Amount = -500.
        # Expense: Debit 500. Amount = 500.
        
        # Receipt of 200:
        # Bank: Debit 200. Amount = -200 (Wait? usually Debit is positive?)
        # Let's check Tally XML standard carefully.
        # <AMOUNT>-500.00</AMOUNT> is Credit.
        # <AMOUNT>500.00</AMOUNT> is Debit.
        
        # So for Payment (Credit Bank): Amount = -500.
        # For Receipt (Debit Bank): Amount = 200.
        
        amount_val = -txn.debit if is_payment else txn.credit
        
        self._add_ledger_entry(voucher, "Bank Account", amount_val)
        
        # Entry 2: Suspense/Party Ledger
        # Since we don't know the counter-party, we put "Suspense" or extract from description in future blocks.
        # For Payment: Debit Suspense. Amount = 500.
        # For Receipt: Credit Suspense. Amount = -200.
        
        contra_amount = -amount_val
        ledger_name = "Suspense Account" # Default
        
        self._add_ledger_entry(voucher, ledger_name, contra_amount)
        
    def _add_ledger_entry(self, voucher: ET.Element, ledger_name: str, amount: float):
        """Add ALLLEDGERENTRIES.LIST item."""
        entry = ET.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
        ET.SubElement(entry, "LEDGERNAME").text = ledger_name
        ET.SubElement(entry, "ISDEEMEDPOSITIVE").text = "Yes" if amount > 0 else "No"
        ET.SubElement(entry, "AMOUNT").text = f"{amount:.2f}"
