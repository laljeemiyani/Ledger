"""Standard Generic Adapter using auto-detection."""

from typing import List
import pandas as pd
from .base import BankAdapter, Transaction
from parsers.csv_parser import CSVParser


class StandardAdapter(BankAdapter):
    """
    Standard adapter that uses auto-detection logic similar to CSVParser.
    Used for Generic/Unknown banks or simple formats.
    """
    
    def process(self) -> List[Transaction]:
        """Process data using column auto-detection."""
        # Use CSVParser's detection logic (reused here directly or we could refactor)
        # We need to map the dataframe columns to standard fields
        
        # Instantiate a dummy parser just to access detection logic? 
        # Or better, copy the logic or move detection to a util. 
        # For now, I'll basically implement a lightweight detection here 
        # or assume the dataframe already has standard columns if mapped?
        # No, the Adapter's job IS to map them.
        
        # Let's re-implement checking logic for flexibility
        column_map = self._detect_columns()
        
        transactions = []
        
        for _, row in self.df.iterrows():
            # Extract fields using map
            date_val = row.get(column_map.get('date'))
            desc_val = row.get(column_map.get('description'))
            
            debit = 0.0
            credit = 0.0
            
            if 'debit' in column_map and 'credit' in column_map:
                debit = self._clean_amount(row.get(column_map.get('debit')))
                credit = self._clean_amount(row.get(column_map.get('credit')))
            elif 'amount' in column_map:
                # Sign based amount logic? or Dr/Cr columns?
                # For generic, standard implementation usually assumes separate cols
                # If single col, we need logic to determine sign.
                # Assuming positive is credit, negative is debit? Or separate logic.
                amount = self._clean_amount(row.get(column_map.get('amount')))
                if amount < 0:
                    debit = abs(amount)
                else:
                    credit = amount
            
            balance = self._clean_amount(row.get(column_map.get('balance'))) if 'balance' in column_map else 0.0
            
            dt = self._parse_date(date_val)
            if dt:
                txn = Transaction(
                    date=dt,
                    description=str(desc_val) if pd.notna(desc_val) else "",
                    debit=debit,
                    credit=credit,
                    balance=balance
                )
                transactions.append(txn)
                
        self.transactions = transactions
        return transactions

    def _detect_columns(self) -> dict:
        """Detect standard columns in the dataframe."""
        # Simplified version of CSVParser.detect_columns logic
        # Ideally this logic should reside in a shared utility.
        # But for now I'll duplicate the keywords list which is robust.
        
        column_map = {}
        cols = {str(c).lower().strip(): c for c in self.df.columns}
        
        keywords = {
            'date': ['date', 'txn date', 'transaction date', 'value date'],
            'description': ['description', 'narration', 'details', 'particulars', 'remarks'],
            'debit': ['debit', 'withdrawal', 'dr', 'paid'],
            'credit': ['credit', 'deposit', 'cr', 'received'],
            'balance': ['balance', 'closing balance'],
            'amount': ['amount', 'txn amount']
        }
        
        for field, keys in keywords.items():
            for key in keys:
                if key in cols:
                    column_map[field] = cols[key]
                    break
                    
        return column_map
