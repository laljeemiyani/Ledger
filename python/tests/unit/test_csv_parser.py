"""Unit tests for CSV Parser module."""

import pytest
from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from parsers.csv_parser import CSVParser


class TestCSVParser:
    """Test cases for CSVParser class."""
    
    def test_invalid_file_path(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with pytest.raises(FileNotFoundError):
            parser = CSVParser('nonexistent.csv')
    
    def test_csv_parser_initialization(self, tmp_path):
        """Test CSVParser can be initialized with valid path."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("col1,col2,col3\nval1,val2,val3")
        
        parser = CSVParser(str(csv_file))
        assert parser.csv_path == csv_file
    
    def test_detect_comma_delimiter(self, tmp_path):
        """Test delimiter detection for comma-separated files."""
        csv_file = tmp_path / "comma.csv"
        csv_file.write_text("date,description,amount\n2024-01-01,Test,100.00")
        
        parser = CSVParser(str(csv_file))
        delimiter = parser.detect_delimiter()
        assert delimiter == ','
    
    def test_detect_semicolon_delimiter(self, tmp_path):
        """Test delimiter detection for semicolon-separated files."""
        csv_file = tmp_path / "semicolon.csv"
        csv_file.write_text("date;description;amount\n2024-01-01;Test;100.00")
        
        parser = CSVParser(str(csv_file))
        delimiter = parser.detect_delimiter()
        assert delimiter == ';'
    
    def test_parse_csv(self, tmp_path):
        """Test parsing valid CSV file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("Date,Description,Debit,Credit,Balance\n2024-01-01,Purchase,100,,1900\n2024-01-02,Salary,,5000,6900")
        
        parser = CSVParser(str(csv_file))
        df = parser.parse()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert len(df.columns) == 5
    
    def test_validate_empty_csv(self, tmp_path):
        """Test validation fails for empty CSV."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("col1,col2,col3\n")
        
        parser = CSVParser(str(csv_file))
        with pytest.raises(ValueError, match="CSV has no data rows"):
            parser.validate_structure()
    
    def test_validate_insufficient_columns(self, tmp_path):
        """Test validation fails for insufficient columns."""
        csv_file = tmp_path / "insufficient.csv"
        csv_file.write_text("col1,col2\nval1,val2")
        
        parser = CSVParser(str(csv_file))
        with pytest.raises(ValueError, match="insufficient columns"):
            parser.validate_structure()
    
    def test_detect_columns(self, tmp_path):
        """Test column detection for bank statement CSV."""
        csv_file = tmp_path / "statement.csv"
        csv_file.write_text("Date,Description,Debit,Credit,Balance\n2024-01-01,Test,100,,1900")
        
        parser = CSVParser(str(csv_file))
        df = parser.parse()
        column_map = parser.detect_columns(df)
        
        assert 'date' in column_map
        assert 'description' in column_map
        assert 'debit' in column_map
        assert 'credit' in column_map
        assert 'balance' in column_map
    
    def test_get_info(self, tmp_path):
        """Test getting CSV file information."""
        csv_file = tmp_path / "info.csv"
        csv_file.write_text("Date,Description,Amount\n2024-01-01,Test,100\n2024-01-02,Test2,200")
        
        parser = CSVParser(str(csv_file))
        info = parser.get_info()
        
        assert info['num_rows'] == 2
        assert info['num_columns'] == 3
        assert info['detected_delimiter'] == ','
        assert info['is_valid'] == True
