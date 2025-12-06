"""SBI Bank Adapter."""

from typing import List
from .base import BankAdapter, Transaction

class SBIAdapter(BankAdapter):
    """Adapter for State Bank of India statements."""
    
    def process(self) -> List[Transaction]:
        """
        Process SBI statement.
        SBI columns usually: Txn Date, Value Date, Description, Ref No./Cheque No., Debit, Credit, Balance
        """
        # Column mapping logic specific to SBI
        # Note: We rely on the dataframe being clean-ish (headers likely on row 0 or 1)
        # But for this implementation we assume the DF passed is the data table
        
        cols = {str(c).lower().strip(): c for c in self.df.columns}
        
        # Simple mapping for standard SBI format
        map_conf = {
            'date': next((cols[c] for c in cols if 'txn date' in c or 'transaction date' in c), None),
            'desc': next((cols[c] for c in cols if 'description' in c or 'narration' in c or 'remarks' in c), None),
            'debit': next((cols[c] for c in cols if 'debit' in c or 'withdrawal' in c), None),
            'credit': next((cols[c] for c in cols if 'credit' in c or 'deposit' in c), None),
            'balance': next((cols[c] for c in cols if 'balance' in c), None),
            'ref': next((cols[c] for c in cols if 'ref' in c or 'cheque' in c), None)
        }
        
        transactions = []
        for _, row in self.df.iterrows():
            # Skip rows that don't look like transactions (e.g. if date is missing)
            date_val = row.get(map_conf['date'])
            if not date_val: 
                continue
                
            dt = self._parse_date(date_val)
            if not dt:
                continue
                
            debit = self._clean_amount(row.get(map_conf['debit']))
            credit = self._clean_amount(row.get(map_conf['credit']))
            balance = self._clean_amount(row.get(map_conf['balance']))
            desc = str(row.get(map_conf['desc']) or '')
            ref = str(row.get(map_conf['ref']) or '')
            
            txn = Transaction(
                date=dt,
                description=desc,
                debit=debit,
                credit=credit,
                balance=balance,
                reference_no=ref
            )
            transactions.append(txn)
            
        self.transactions = transactions
        return transactions
