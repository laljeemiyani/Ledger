"""CSV Parser Module for processing bank statement CSV files."""

from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import csv


class CSVParser:
    """Handles parsing and validation of CSV bank statements."""
    
    def __init__(self, csv_path: str) -> None:
        """
        Initialize CSV parser.
        
        Args:
            csv_path: Path to the CSV file
        """
        self.csv_path = Path(csv_path)
        
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    def detect_delimiter(self) -> str:
        """
        Auto-detect CSV delimiter.
        
        Returns:
            Detected delimiter character (comma, semicolon, tab, or pipe)
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                # Read first few lines
                sample = file.read(4096)
                
                # Use csv.Sniffer to detect delimiter
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
                return dialect.delimiter
                
        except Exception as e:
            # Fallback to comma
            return ','
    
    def parse(self, delimiter: Optional[str] = None) -> pd.DataFrame:
        """
        Parse CSV file into DataFrame.
        
        Args:
            delimiter: Optional delimiter. If None, auto-detects.
            
        Returns:
            pandas DataFrame containing parsed CSV data
        """
        try:
            if delimiter is None:
                delimiter = self.detect_delimiter()
            
            # Read CSV with pandas
            df = pd.read_csv(
                self.csv_path,
                delimiter=delimiter,
                encoding='utf-8',
                parse_dates=False,  # We'll handle date parsing later
                low_memory=False
            )
            
            # Remove completely empty rows and columns
            df = df.dropna(how='all')
            df = df.dropna(axis=1, how='all')
            
            return df
            
        except Exception as e:
            raise RuntimeError(f"Error parsing CSV: {str(e)}")
    
    def validate_structure(self, df: Optional[pd.DataFrame] = None) -> bool:
        """
        Validate that CSV has expected bank statement structure.
        
        Args:
            df: Optional DataFrame. If None, parses file first.
            
        Returns:
            True if structure is valid
            
        Raises:
            ValueError: If structure is invalid
        """
        if df is None:
            df = self.parse()
        
        # Check if DataFrame is empty
        if df.empty:
            raise ValueError("CSV file is empty")
        
        # Check minimum number of columns (at least 3: date, description, amount)
        if len(df.columns) < 3:
            raise ValueError(
                f"CSV has insufficient columns. Expected at least 3, got {len(df.columns)}"
            )
        
        # Check minimum number of rows (at least 1 data row)
        if len(df) < 1:
            raise ValueError("CSV has no data rows")
        
        return True
    
    def detect_columns(self, df: Optional[pd.DataFrame] = None) -> Dict[str, str]:
        """
        Detect which columns contain date, description, amount, and balance.
        
        Args:
            df: Optional DataFrame. If None, parses file first.
            
        Returns:
            Dictionary mapping field names to column names
        """
        if df is None:
            df = self.parse()
        
        column_map = {}
        
        # Common date column keywords
        date_keywords = ['date', 'txn date', 'transaction date', 'value date', 'posting date']
        # Common description keywords
        desc_keywords = ['description', 'narration', 'details', 'particulars', 'remarks']
        # Common debit/credit keywords
        debit_keywords = ['debit', 'withdrawal', 'dr', 'paid', 'amount paid']
        credit_keywords = ['credit', 'deposit', 'cr', 'received', 'amount received']
        # Common amount keywords (when single amount column)
        amount_keywords = ['amount', 'transaction amount', 'txn amount']
        # Common balance keywords
        balance_keywords = ['balance', 'closing balance', 'running balance']
        
        # Normalize column names for matching
        normalized_cols = {col.lower().strip(): col for col in df.columns}
        
        # Detect date column
        for keyword in date_keywords:
            if keyword in normalized_cols:
                column_map['date'] = normalized_cols[keyword]
                break
        
        # Detect description column
        for keyword in desc_keywords:
            if keyword in normalized_cols:
                column_map['description'] = normalized_cols[keyword]
                break
        
        # Detect amount columns (debit/credit or single amount)
        for keyword in debit_keywords:
            if keyword in normalized_cols:
                column_map['debit'] = normalized_cols[keyword]
                break
        
        for keyword in credit_keywords:
            if keyword in normalized_cols:
                column_map['credit'] = normalized_cols[keyword]
                break
        
        # If no debit/credit, look for single amount column
        if 'debit' not in column_map and 'credit' not in column_map:
            for keyword in amount_keywords:
                if keyword in normalized_cols:
                    column_map['amount'] = normalized_cols[keyword]
                    break
        
        # Detect balance column
        for keyword in balance_keywords:
            if keyword in normalized_cols:
                column_map['balance'] = normalized_cols[keyword]
                break
        
        return column_map
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get CSV file information.
        
        Returns:
            Dictionary containing file info
        """
        df = self.parse()
        column_map = self.detect_columns(df)
        
        return {
            'file_path': str(self.csv_path),
            'num_rows': len(df),
            'num_columns': len(df.columns),
            'columns': list(df.columns),
            'detected_delimiter': self.detect_delimiter(),
            'column_mapping': column_map,
            'is_valid': self.validate_structure(df),
        }
