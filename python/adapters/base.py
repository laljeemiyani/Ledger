"""Base Adapter module defining the interface for bank adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Dict, Optional
import pandas as pd


@dataclass
class Transaction:
    """Standardized transaction entry."""
    date: datetime
    description: str
    debit: float
    credit: float
    balance: float
    reference_no: Optional[str] = None
    value_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            'date': self.date.isoformat(),
            'description': self.description,
            'debit': self.debit,
            'credit': self.credit,
            'balance': self.balance,
            'reference_no': self.reference_no,
            'value_date': self.value_date.isoformat() if self.value_date else None
        }


class BankAdapter(ABC):
    """Abstract Base Class for all bank adapters."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize adapter with raw data.
        
        Args:
            data: pandas DataFrame containing raw statement data
        """
        self.df = data
        self.transactions: List[Transaction] = []
        
    @abstractmethod
    def process(self) -> List[Transaction]:
        """
        Process the raw data and extract standardized transactions.
        
        Returns:
            List of Transaction objects
        """
        pass
    
    def validate(self) -> bool:
        """
        Validate if the data matches the expected format for this adapter.
        
        Returns:
            True if valid
        """
        return True
    
    def _clean_amount(self, value: Any) -> float:
        """Helper to clean and convert amount strings to float."""
        if pd.isna(value) or value == '':
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        
        # Remove currency symbols, commas, and whitespace
        clean_str = str(value).replace(',', '').replace('₹', '').strip()
        
        # Handle "Cr"/"Dr" suffixes if present
        if clean_str.lower().endswith('cr'):
            clean_str = clean_str[:-2].strip()
        elif clean_str.lower().endswith('dr'):
            clean_str = clean_str[:-2].strip()
            
        try:
            return float(clean_str)
        except ValueError:
            return 0.0

    def _parse_date(self, value: Any, date_format: Optional[str] = None) -> Optional[datetime]:
        """Helper to parse date strings."""
        if pd.isna(value) or value == '':
            return None
        
        try:
            if isinstance(value, datetime):
                return value
            
            # If it's a pandas Timestamp
            if hasattr(value, 'to_pydatetime'):
                return value.to_pydatetime()
                
            clean_str = str(value).strip()
            if date_format:
                return datetime.strptime(clean_str, date_format)
            
            # Auto-parse using pandas
            return pd.to_datetime(clean_str).to_pydatetime()
            
        except (ValueError, TypeError):
            return None
