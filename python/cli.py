"""CLI Entry point for Ledger Processing."""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from parsers.csv_parser import CSVParser
from parsers.excel_parser import ExcelParser
from parsers.bank_detector import BankDetector
from adapters.factory import AdapterFactory
# For PDF and OCR, we'd import/implement wrappers here
# Currently we focus on the integration structure
# from pdf_processor.reader import PDFReader (Already exists, but needs integration logic)

def process_file(file_path: str) -> Dict[str, Any]:
    """Process a single file and return result."""
    path = Path(file_path)
    if not path.exists():
        return {'file': file_path, 'status': 'error', 'message': 'File not found'}
    
    try:
        # 1. Determine File Type
        suffix = path.suffix.lower()
        
        df = None
        raw_text = ""
        
        # 2. Extract Data (Simulated for generic logic for now, using existing parsers)
        if suffix == '.csv':
            parser = CSVParser(str(path))
            df = parser.parse()
            # Simulation: We don't extract raw text from CSV easily for detection unless we convert to string
            # For detection, we might just look at headers
            raw_text = ",".join(df.columns) 
        elif suffix in ['.xls', '.xlsx']:
            parser = ExcelParser(str(path))
            df = parser.parse()
            raw_text = ",".join(df.columns)
        elif suffix == '.pdf':
            # TODO: Integrate PDFReader
            return {'file': file_path, 'status': 'error', 'message': 'PDF processing not yet fully wired in CLI'}
        elif suffix in ['.png', '.jpg', '.jpeg']:
            # TODO: Integrate OCR
            return {'file': file_path, 'status': 'error', 'message': 'Image processing not yet fully wired in CLI'}
        else:
            return {'file': file_path, 'status': 'error', 'message': 'Unsupported file type'}
            
        # 3. Detect Bank
        bank = BankDetector.detect(raw_text) or ""
        
        # 4. Standardize
        adapter = AdapterFactory.get_adapter(bank, df)
        transactions = adapter.process()
        
        return {
            'file': file_path,
            'status': 'success',
            'bank': bank,
            'transaction_count': len(transactions),
            'transactions': [txn.to_dict() for txn in transactions]
        }
        
    except Exception as e:
        return {'file': file_path, 'status': 'error', 'message': str(e)}

def main():
    parser = argparse.ArgumentParser(description="Process bank statements.")
    parser.add_argument('files', nargs='+', help="List of file paths to process")
    
    args = parser.parse_args()
    
    results = []
    for file_path in args.files:
        result = process_file(file_path)
        results.append(result)
        
    # Output JSON to stdout
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
