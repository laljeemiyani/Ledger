"""Unit tests for Excel Parser module."""

import pytest
from pathlib import Path
import sys
import pandas as pd
import openpyxl

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from parsers.excel_parser import ExcelParser


class TestExcelParser:
    """Test cases for ExcelParser class."""
    
    @pytest.fixture
    def sample_xlsx(self, tmp_path):
        """Create a sample Excel file."""
        file_path = tmp_path / "test.xlsx"
        
        # Create a DataFrame and save as Excel
        df = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02'],
            'Description': ['Test 1', 'Test 2'],
            'Debit': [100, None],
            'Credit': [None, 200],
            'Balance': [1000, 1200]
        })
        
        df.to_excel(file_path, index=False)
        return file_path

    def test_invalid_file_path(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with pytest.raises(FileNotFoundError):
            parser = ExcelParser('nonexistent.xlsx')
    
    def test_excel_parser_initialization(self, sample_xlsx):
        """Test ExcelParser can be initialized with valid path."""
        parser = ExcelParser(str(sample_xlsx))
        assert parser.excel_path == sample_xlsx
    
    def test_get_sheet_names(self, sample_xlsx):
        """Test retrieving sheet names."""
        parser = ExcelParser(str(sample_xlsx))
        sheets = parser.get_sheet_names()
        
        assert len(sheets) == 1
        assert "Sheet1" in sheets
    
    def test_parse_excel(self, sample_xlsx):
        """Test parsing Excel file into DataFrame."""
        parser = ExcelParser(str(sample_xlsx))
        df = parser.parse()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        # pandas often reads numbers as floats if NaNs are present, but we force str in parse
        # Note: df.to_excel writes standard types, read_excel with dtype=str reads strings
        assert 'Date' in df.columns
        assert 'Balance' in df.columns
        
    def test_validate_empty_excel(self, tmp_path):
        """Test validation fails for empty Excel sheet."""
        file_path = tmp_path / "empty.xlsx"
        pd.DataFrame().to_excel(file_path, index=False)
        
        parser = ExcelParser(str(file_path))
        # Empty dataframe to_excel writes header only? or nothing?
        # Usually writes nothing if columns empty.
        
        with pytest.raises(ValueError, match="Excel sheet is empty"):
            parser.validate_structure()
            
    def test_validate_insufficient_columns(self, tmp_path):
        """Test validation fails for insufficient columns."""
        file_path = tmp_path / "insufficient.xlsx"
        pd.DataFrame({'A': [1], 'B': [2]}).to_excel(file_path, index=False)
        
        parser = ExcelParser(str(file_path))
        with pytest.raises(ValueError, match="insufficient columns"):
            parser.validate_structure()
            
    def test_detect_columns(self, sample_xlsx):
        """Test column detection."""
        parser = ExcelParser(str(sample_xlsx))
        column_map = parser.detect_columns()
        
        assert column_map['date'] == 'Date'
        assert column_map['description'] == 'Description'
        assert column_map['debit'] == 'Debit'
        assert column_map['credit'] == 'Credit'
        assert column_map['balance'] == 'Balance'
        
    def test_get_info(self, sample_xlsx):
        """Test getting file info."""
        parser = ExcelParser(str(sample_xlsx))
        info = parser.get_info()
        
        assert info['num_sheets'] == 1
        assert info['num_rows'] == 2
        assert info['is_valid'] == True
        assert 'Date' in info['columns']
