"""Excel Parser Module for processing bank statement Excel files."""

from typing import Optional, List, Dict, Any, Union
from pathlib import Path
import pandas as pd
import openpyxl


class ExcelParser:
    """Handles parsing and validation of Excel bank statements."""
    
    def __init__(self, excel_path: str) -> None:
        """
        Initialize Excel parser.
        
        Args:
            excel_path: Path to the Excel file
        """
        self.excel_path = Path(excel_path)
        
        if not self.excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    def get_sheet_names(self) -> List[str]:
        """
        Get list of sheet names in the Excel file.
        
        Returns:
            List of sheet names
        """
        try:
            with pd.ExcelFile(self.excel_path) as xls:
                return xls.sheet_names
        except Exception as e:
            raise RuntimeError(f"Error reading Excel sheets: {str(e)}")
    
    def parse(self, sheet_name: Optional[Union[str, int]] = 0) -> pd.DataFrame:
        """
        Parse Excel sheet into DataFrame.
        
        Args:
            sheet_name: Sheet name or index (default 0 for first sheet)
            
        Returns:
            pandas DataFrame containing parsed data
        """
        try:
            # Read Excel with pandas
            # openpyxl engine is used for xlsx
            df = pd.read_excel(
                self.excel_path,
                sheet_name=sheet_name,
                parse_dates=False,
                dtype=str  # Read all as string to preserve formatting
            )
            
            # Remove completely empty rows and columns
            df = df.dropna(how='all')
            df = df.dropna(axis=1, how='all')
            
            return df
            
        except Exception as e:
            raise RuntimeError(f"Error parsing Excel: {str(e)}")
    
    def validate_structure(self, df: Optional[pd.DataFrame] = None) -> bool:
        """
        Validate that Excel sheet has expected bank statement structure.
        
        Args:
            df: Optional DataFrame. If None, parses first sheet.
            
        Returns:
            True if structure is valid
            
        Raises:
            ValueError: If structure is invalid
        """
        if df is None:
            df = self.parse()
        
        # Check if DataFrame is empty
        if df.empty:
            raise ValueError("Excel sheet is empty")
        
        # Check minimum number of columns (at least 3: date, description, amount)
        if len(df.columns) < 3:
            raise ValueError(
                f"Excel sheet has insufficient columns. Expected at least 3, got {len(df.columns)}"
            )
        
        # Check minimum number of rows (at least 1 data row)
        if len(df) < 1:
            raise ValueError("Excel sheet has no data rows")
        
        return True
    
    def detect_columns(self, df: Optional[pd.DataFrame] = None) -> Dict[str, str]:
        """
        Detect which columns contain date, description, amount, and balance.
        
        Args:
            df: Optional DataFrame. If None, parses first sheet.
            
        Returns:
            Dictionary mapping field names to column names
        """
        if df is None:
            df = self.parse()
        
        column_map = {}
        
        # Reuse keywords from CSV parser (could refactor to shared util)
        date_keywords = ['date', 'txn date', 'transaction date', 'value date', 'posting date']
        desc_keywords = ['description', 'narration', 'details', 'particulars', 'remarks']
        debit_keywords = ['debit', 'withdrawal', 'dr', 'paid', 'amount paid']
        credit_keywords = ['credit', 'deposit', 'cr', 'received', 'amount received']
        amount_keywords = ['amount', 'transaction amount', 'txn amount']
        balance_keywords = ['balance', 'closing balance', 'running balance']
        
        # Normalize column names for matching
        # Convert to string first just in case
        normalized_cols = {str(col).lower().strip(): col for col in df.columns}
        
        # Helper to find column
        def find_col(keywords: List[str]) -> Optional[str]:
            for keyword in keywords:
                if keyword in normalized_cols:
                    return normalized_cols[keyword]
            return None
            
        col = find_col(date_keywords)
        if col: column_map['date'] = col
        
        col = find_col(desc_keywords)
        if col: column_map['description'] = col
        
        col = find_col(debit_keywords)
        if col: column_map['debit'] = col
        
        col = find_col(credit_keywords)
        if col: column_map['credit'] = col
        
        if 'debit' not in column_map and 'credit' not in column_map:
            col = find_col(amount_keywords)
            if col: column_map['amount'] = col
            
        col = find_col(balance_keywords)
        if col: column_map['balance'] = col
        
        return column_map
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get Excel file information.
        
        Returns:
            Dictionary containing file info
        """
        sheet_names = self.get_sheet_names()
        
        # Parse first sheet for details
        df = self.parse()
        column_map = self.detect_columns(df)
        
        return {
            'file_path': str(self.excel_path),
            'sheet_names': sheet_names,
            'num_sheets': len(sheet_names),
            'num_rows': len(df),
            'num_columns': len(df.columns),
            'columns': list(df.columns),
            'column_mapping': column_map,
            'is_valid': self.validate_structure(df),
        }
