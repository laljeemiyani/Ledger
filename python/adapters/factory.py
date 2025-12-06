"""Factory for creating bank adapters."""

from typing import Type
import pandas as pd
from .base import BankAdapter
from .sbi_adapter import SBIAdapter
from .std_adapter import StandardAdapter

class AdapterFactory:
    """Factory to get the appropriate adapter."""
    
    @staticmethod
    def get_adapter(bank_name: str, data: pd.DataFrame) -> BankAdapter:
        """
        Get adapter instance for the specified bank.
        
        Args:
            bank_name: Name of the bank (detected by BankDetector)
            data: Raw DataFrame
            
        Returns:
            Instance of BankAdapter subclass
        """
        bank = bank_name.upper() if bank_name else ""
        
        if bank == 'SBI':
            return SBIAdapter(data)
        # elif bank == 'HDFC':
        #     return HDFCAdapter(data)
        
        # Default to standard adapter
        return StandardAdapter(data)
