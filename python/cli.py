"""CLI Entry point for Ledger Processing."""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime
from parsers.csv_parser import CSVParser
from parsers.excel_parser import ExcelParser
from parsers.bank_detector import BankDetector
from adapters.factory import AdapterFactory
from adapters.base import Transaction
from exporters.tally_xml import TallyXMLExporter

def process_file(file_path: str) -> Dict[str, Any]:
    # ... (existing content, no change in logic, just indentation if inside class but here it's function)
    # Keeping existing logic.
    path = Path(file_path)
    if not path.exists():
        return {'file': file_path, 'status': 'error', 'message': 'File not found'}
    
    try:
        suffix = path.suffix.lower()
        df = None
        raw_text = ""
        
        if suffix == '.csv':
            parser = CSVParser(str(path))
            df = parser.parse()
            raw_text = ",".join(df.columns) 
        elif suffix in ['.xls', '.xlsx']:
            parser = ExcelParser(str(path))
            df = parser.parse()
            raw_text = ",".join(df.columns)
        else:
            return {'file': file_path, 'status': 'error', 'message': 'Unsupported file type'}
            
        bank = BankDetector.detect(raw_text) or ""
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

def handle_export(format_type: str):
    """Read transactions from stdin and export."""
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({'success': False, 'message': 'No input data'}))
            return

        txns_data = json.loads(input_data)
        
        # Convert dicts back to Transaction objects
        transactions = []
        for t in txns_data:
            transactions.append(Transaction(
                date=datetime.fromisoformat(t['date']),
                description=t.get('description', ''),
                debit=float(t.get('debit', 0)),
                credit=float(t.get('credit', 0)),
                balance=float(t.get('balance', 0)),
                reference_no=t.get('reference_no'),
                value_date=datetime.fromisoformat(t['value_date']) if t.get('value_date') else None
            ))
            
        if format_type == 'tally-xml':
            exporter = TallyXMLExporter(transactions)
            xml_content = exporter.generate_xml()
            print(json.dumps({'success': True, 'content': xml_content}))
        else:
            print(json.dumps({'success': False, 'message': f'Unknown format: {format_type}'}))
            
    except Exception as e:
        print(json.dumps({'success': False, 'message': str(e)}))

def main():
    parser = argparse.ArgumentParser(description="Process bank statements.")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Process Command
    proc_parser = subparsers.add_parser('process', help='Process files')
    proc_parser.add_argument('files', nargs='+', help="List of file paths")
    
    # Export Command
    exp_parser = subparsers.add_parser('export', help='Export transactions')
    exp_parser.add_argument('--format', required=True, help="Export format (e.g. tally-xml)")
    
    args = parser.parse_args()
    
    if args.command == 'process':
        results = []
        for file_path in args.files:
            result = process_file(file_path)
            results.append(result)
        print(json.dumps(results, indent=2))
        
    elif args.command == 'export':
        handle_export(args.format)
        
    else:
        # Default behavior for backward compatibility or error
        if hasattr(args, 'files'):
             # If just files passed without subcommand (old behavior)
             # But argparse won't let us here easily without subcommand if defined.
             # Actually, if I define subparsers, it might be strict.
             # I'll rely on 'process' subcommand being used.
             parser.print_help()
        else:
             parser.print_help()

if __name__ == '__main__':
    main()
