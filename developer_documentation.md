# Developer Documentation

## PDF Bank Statement to Tally XML/Excel Converter

---

## 📚 Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Module Breakdown](#module-breakdown)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
7. [PDF Processing Logic](#pdf-processing-logic)
8. [XML Generation](#xml-generation)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Guide](#deployment-guide)

---

## 🛠️ Development Environment Setup

### Prerequisites

```bash
# Required Software
- Node.js (v18.x or higher)
- Python 3.10+
- Git
- VS Code or preferred IDE

# For Desktop App (Electron)
- npm or yarn
- Electron 25+

# For Web Version
- React 18+
- Vite or Create React App
```

### Installation Steps

```bash
# Clone repository
git clone https://github.com/yourusername/bank-statement-converter.git
cd bank-statement-converter

# Install frontend dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Run development server
npm run dev
```

### Environment Variables

```env
# .env file
NODE_ENV=development
PYTHON_PATH=/usr/bin/python3
PDF_TEMP_DIR=./temp/pdfs
OUTPUT_DIR=./output
MAX_FILE_SIZE=52428800  # 50MB in bytes
SUPPORTED_BANKS=SBI,HDFC,ICICI,AXIS,KOTAK,PNB,BOB,CANARA,UNION,INDUSIND
LOG_LEVEL=debug
```

---

## 🏗️ Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface (React/Electron)        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │  Upload  │  │ Preview  │  │ Mapping  │  │ Export   ││
│  │  Module  │  │  Editor  │  │  Engine  │  │ Module   ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
└─────────────────────────┬───────────────────────────────┘
                          │
                    (IPC/API Calls)
                          │
┌─────────────────────────▼───────────────────────────────┐
│              Application Logic Layer (Node.js)            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  File        │  │  Processing  │  │  Configuration ││
│  │  Manager     │  │  Orchestrator│  │  Manager       ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
└─────────────────────────┬───────────────────────────────┘
                          │
              (Python Bridge via Child Process)
                          │
┌─────────────────────────▼───────────────────────────────┐
│               PDF Processing Layer (Python)               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  PDF Parser  │  │  Table       │  │  OCR Engine    ││
│  │              │  │  Extractor   │  │  (Tesseract)   ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
└─────────────────────────┬───────────────────────────────┘
                          │
              (Structured Data Output)
                          │
┌─────────────────────────▼───────────────────────────────┐
│               Data Processing Layer (Node.js)             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  Validator   │  │  Ledger      │  │  Format        ││
│  │              │  │  Mapper      │  │  Converter     ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
└─────────────────────────┬───────────────────────────────┘
                          │
                (Output Generation)
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 Output Generation Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  XML         │  │  Excel       │  │  CSV           ││
│  │  Generator   │  │  Generator   │  │  Generator     ││
│  └──────────────┘  └──────────────┘  └────────────────┘│
└───────────────────────────────────────────────────────────┘
```

### Design Patterns

1. **Adapter Pattern**: For different bank statement formats
2. **Factory Pattern**: For creating PDF parsers based on bank type
3. **Strategy Pattern**: For different extraction strategies
4. **Observer Pattern**: For progress updates and notifications
5. **Singleton Pattern**: For configuration and logger instances

---

## 💻 Technology Stack

### Frontend

```javascript
// Core Framework
- React 18.2.0
- TypeScript 5.0
- Electron 25.x (for desktop)

// UI Components
- Tailwind CSS 3.x
- shadcn/ui components
- React Hook Form
- Zod (validation)

// State Management
- Zustand or Redux Toolkit
- React Query (for async state)

// Utilities
- date-fns (date manipulation)
- lodash (utility functions)
- react-dropzone (file upload)
```

### Backend (Node.js)

```javascript
// Runtime
- Node.js 18.x
- TypeScript 5.x

// Framework
- Express.js 4.x (if web API needed)

// PDF Processing Bridge
- child_process (Python integration)
- node-ipc (process communication)

// Data Processing
- xlsx (Excel generation)
- fast-xml-parser (XML generation)
- date-fns

// Database
- better-sqlite3 (local storage)
- TypeORM (if using database)
```

### PDF Processing (Python)

```python
# PDF Libraries
- PyPDF2 4.x          # PDF reading
- pdfplumber 0.10.x   # Table extraction
- tabula-py 2.8.x     # Advanced table extraction
- camelot-py 0.11.x   # Alternative table extraction

# OCR
- pytesseract 0.3.x   # OCR engine wrapper
- Pillow 10.x         # Image processing
- opencv-python       # Image preprocessing

# Data Processing
- pandas 2.x          # Data manipulation
- numpy 1.24.x        # Numerical operations
- python-dateutil     # Date parsing

# Utilities
- regex              # Advanced pattern matching
- pycryptodome       # PDF password handling
```

---

## 📦 Module Breakdown

### 1. File Upload Module (`/src/modules/upload`)

**Responsibilities**:

- Handle file selection/drag-drop
- Validate file type and size
- Detect password protection
- Queue files for processing

**Key Files**:

```
upload/
├── FileUploader.tsx          # Main upload component
├── PasswordPrompt.tsx        # Password input dialog
├── FileQueue.tsx             # File list management
├── validators.ts             # File validation logic
└── types.ts                  # TypeScript interfaces
```

**Core Functions**:

```typescript
// File validation
interface FileValidator {
  validateFileType(file: File): boolean;
  validateFileSize(file: File): boolean;
  detectPasswordProtection(file: File): Promise<boolean>;
  validatePDF(file: File): Promise<boolean>;
  validateImage(file: File): Promise<boolean>;
  validateCSV(file: File): Promise<boolean>;
  validateExcel(file: File): Promise<boolean>;
}

// File queue management
interface FileQueue {
  addFiles(files: File[]): void;
  removeFile(fileId: string): void;
  getQueueStatus(): QueueStatus;
  clearQueue(): void;
  getFilesByType(type: "pdf" | "image" | "csv" | "excel"): File[];
}
```

---

### 2. PDF Processing Module (`/python/pdf_processor`)

**Responsibilities**:

- Parse PDF structure
- Extract text and tables
- Handle encrypted PDFs
- Perform OCR if needed

**Key Files**:

```
pdf_processor/
├── __init__.py
├── parser.py                 # Main PDF parser
├── bank_detector.py          # Auto-detect bank
├── table_extractor.py        # Extract transaction tables
├── ocr_engine.py             # OCR for scanned PDFs
├── password_handler.py       # Handle password-protected PDFs
└── config/
    └── bank_patterns.json    # Bank identification patterns
```

**Core Classes**:

```python
# pdf_processor/parser.py
class PDFParser:
    """Main PDF parsing orchestrator"""

    def __init__(self, pdf_path: str, password: str = None):
        self.pdf_path = pdf_path
        self.password = password
        self.bank_type = None

    def parse(self) -> dict:
        """
        Main parsing method
        Returns: Dictionary with extracted data
        """
        # 1. Detect bank
        self.bank_type = self.detect_bank()

        # 2. Extract tables
        tables = self.extract_tables()

        # 3. Extract metadata
        metadata = self.extract_metadata()

        # 4. Validate and structure data
        structured_data = self.structure_data(tables, metadata)

        return structured_data

    def detect_bank(self) -> str:
        """Auto-detect bank from PDF content"""
        pass

    def extract_tables(self) -> list:
        """Extract transaction tables from PDF"""
        pass

    def extract_metadata(self) -> dict:
        """Extract account info from header"""
        pass


# pdf_processor/bank_detector.py
class BankDetector:
    """Identifies bank from PDF patterns"""

    BANK_PATTERNS = {
        'SBI': {
            'keywords': ['State Bank of India', 'SBI'],
            'ifsc_pattern': r'^SBIN\d{7}$',
            'account_pattern': r'^\d{11}$'
        },
        'HDFC': {
            'keywords': ['HDFC Bank', 'HDFC'],
            'ifsc_pattern': r'^HDFC\d{7}$',
            'account_pattern': r'^\d{14}$'
        },
        # ... other banks
    }

    def detect(self, pdf_text: str, metadata: dict) -> str:
        """
        Returns: Bank name (SBI, HDFC, etc.) or 'UNKNOWN'
        """
        pass


# pdf_processor/table_extractor.py
class TableExtractor:
    """Extracts transaction tables using multiple strategies"""

    def __init__(self, strategy: str = 'auto'):
        self.strategy = strategy

    def extract(self, pdf_path: str, pages: list = None) -> pd.DataFrame:
        """
        Extract tables and return as pandas DataFrame
        Tries multiple methods and returns best result
        """
        if self.strategy == 'auto':
            # Try multiple methods
            df = self._try_pdfplumber(pdf_path, pages)
            if df is None:
                df = self._try_tabula(pdf_path, pages)
            if df is None:
                df = self._try_camelot(pdf_path, pages)

        return df

    def _try_pdfplumber(self, pdf_path: str, pages: list) -> pd.DataFrame:
        """Extract using pdfplumber"""
        pass

    def _try_tabula(self, pdf_path: str, pages: list) -> pd.DataFrame:
        """Extract using tabula-py"""
        pass
```

---

### 3. Bank Adapter Module (`/python/adapters`)

**Responsibilities**:

- Bank-specific parsing logic
- Column mapping
- Date format handling
- Transaction type detection

**Structure**:

```
adapters/
├── __init__.py
├── base_adapter.py           # Abstract base adapter
├── sbi_adapter.py
├── hdfc_adapter.py
├── icici_adapter.py
├── axis_adapter.py
└── ... (other banks)
```

**Base Adapter Pattern**:

```python
# adapters/base_adapter.py
from abc import ABC, abstractmethod
import pandas as pd

class BankAdapter(ABC):
    """Abstract base class for bank-specific adapters"""

    BANK_NAME = None
    DATE_FORMAT = '%d/%m/%Y'

    # Column name mappings (PDF → Standard)
    COLUMN_MAPPING = {
        'date': [],           # Possible date column names
        'narration': [],      # Description/Narration columns
        'cheque_no': [],      # Reference number columns
        'debit': [],          # Debit amount columns
        'credit': [],         # Credit amount columns
        'balance': []         # Balance columns
    }

    @abstractmethod
    def parse_statement(self, raw_data: pd.DataFrame) -> dict:
        """
        Convert raw extracted data to standardized format

        Args:
            raw_data: DataFrame from table extractor

        Returns:
            dict: Standardized transaction data
        """
        pass

    def detect_columns(self, df: pd.DataFrame) -> dict:
        """Auto-detect column positions"""
        detected = {}

        for standard_name, possible_names in self.COLUMN_MAPPING.items():
            for col in df.columns:
                if any(name.lower() in col.lower() for name in possible_names):
                    detected[standard_name] = col
                    break

        return detected

    def parse_date(self, date_str: str) -> datetime:
        """Parse date according to bank format"""
        return datetime.strptime(date_str, self.DATE_FORMAT)

    def parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float"""
        # Remove currency symbols, commas
        cleaned = amount_str.replace(',', '').replace('₹', '').strip()
        return float(cleaned) if cleaned else 0.0


# adapters/sbi_adapter.py
class SBIAdapter(BankAdapter):
    """State Bank of India statement adapter"""

    BANK_NAME = 'SBI'
    DATE_FORMAT = '%d %b %Y'  # e.g., 01 Jan 2024

    COLUMN_MAPPING = {
        'date': ['Txn Date', 'Date', 'Transaction Date'],
        'narration': ['Description', 'Narration', 'Particulars'],
        'cheque_no': ['Ref No.', 'Reference', 'Cheque No'],
        'debit': ['Debit', 'Withdrawal', 'Dr'],
        'credit': ['Credit', 'Deposit', 'Cr'],
        'balance': ['Balance', 'Running Balance']
    }

    def parse_statement(self, raw_data: pd.DataFrame) -> dict:
        """SBI-specific parsing logic"""

        # Detect columns
        columns = self.detect_columns(raw_data)

        transactions = []

        for _, row in raw_data.iterrows():
            transaction = {
                'date': self.parse_date(row[columns['date']]),
                'narration': row[columns['narration']],
                'cheque_no': row.get(columns.get('cheque_no', ''), ''),
                'debit': self.parse_amount(row.get(columns.get('debit', ''), '0')),
                'credit': self.parse_amount(row.get(columns.get('credit', ''), '0')),
                'balance': self.parse_amount(row[columns['balance']]),
                'type': self._detect_transaction_type(row)
            }
            transactions.append(transaction)

        return {
            'bank': self.BANK_NAME,
            'transactions': transactions
        }

    def _detect_transaction_type(self, row: pd.Series) -> str:
        """Detect transaction type from narration"""
        narration = row['Narration'].upper()

        if 'UPI' in narration:
            return 'UPI'
        elif 'NEFT' in narration or 'IMPS' in narration:
            return 'ONLINE_TRANSFER'
        elif 'ATM' in narration:
            return 'ATM'
        elif 'CHQ' in narration or 'CHEQUE' in narration:
            return 'CHEQUE'
        else:
            return 'OTHER'
```

---

### 4. Data Validation Module (`/src/modules/validation`)

**Responsibilities**:

- Validate extracted data
- Check balance calculations
- Detect anomalies
- Flag errors for user review

```typescript
// validation/validator.ts
interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

interface ValidationError {
  row: number;
  field: string;
  message: string;
  severity: "error" | "warning";
}

class TransactionValidator {
  validate(transactions: Transaction[]): ValidationResult {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    // 1. Check date sequence
    this.validateDateSequence(transactions, errors);

    // 2. Validate amounts
    this.validateAmounts(transactions, errors);

    // 3. Check balance calculations
    this.validateBalances(transactions, errors);

    // 4. Detect duplicates
    this.detectDuplicates(transactions, warnings);

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  }

  private validateBalances(
    transactions: Transaction[],
    errors: ValidationError[]
  ): void {
    let expectedBalance = transactions[0].openingBalance;

    for (let i = 0; i < transactions.length; i++) {
      const txn = transactions[i];
      expectedBalance = expectedBalance + txn.credit - txn.debit;

      if (Math.abs(expectedBalance - txn.balance) > 0.01) {
        errors.push({
          row: i,
          field: "balance",
          message: `Balance mismatch: Expected ${expectedBalance}, Found ${txn.balance}`,
          severity: "error",
        });
      }
    }
  }
}
```

---

### 5. Ledger Mapping Module (`/src/modules/mapping`)

**Responsibilities**:

- Map transactions to Tally ledgers
- Apply mapping rules
- Learn from user corrections
- Manage mapping templates

```typescript
// mapping/ledger-mapper.ts
interface MappingRule {
  id: string;
  pattern: string | RegExp;
  ledgerName: string;
  voucherType: "Receipt" | "Payment" | "Contra";
  priority: number;
}

class LedgerMapper {
  private rules: MappingRule[] = [];

  constructor() {
    this.loadDefaultRules();
  }

  mapTransaction(transaction: Transaction): MappedTransaction {
    const matchingRule = this.findMatchingRule(transaction.narration);

    return {
      ...transaction,
      ledgerName: matchingRule?.ledgerName || "Uncategorized",
      voucherType: this.determineVoucherType(transaction),
      mappingConfidence: matchingRule ? 1.0 : 0.0,
    };
  }

  private loadDefaultRules(): void {
    this.rules = [
      {
        id: "salary",
        pattern: /salary|income/i,
        ledgerName: "Salary Income",
        voucherType: "Receipt",
        priority: 10,
      },
      {
        id: "upi",
        pattern: /UPI|PhonePe|GooglePay|Paytm/i,
        ledgerName: "UPI Payments",
        voucherType: "Payment",
        priority: 8,
      },
      // ... more rules
    ];
  }

  addRule(rule: MappingRule): void {
    this.rules.push(rule);
    this.rules.sort((a, b) => b.priority - a.priority);
  }

  private findMatchingRule(narration: string): MappingRule | null {
    for (const rule of this.rules) {
      if (typeof rule.pattern === "string") {
        if (narration.toLowerCase().includes(rule.pattern.toLowerCase())) {
          return rule;
        }
      } else if (rule.pattern.test(narration)) {
        return rule;
      }
    }
    return null;
  }
}
```

---

### 6. XML Generation Module (`/src/modules/export`)

**Responsibilities**:

- Generate Tally XML format
- Create voucher entries
- Handle ledger references
- Validate XML structure

```typescript
// export/tally-xml-generator.ts
import { create } from "xmlbuilder2";

interface TallyXMLOptions {
  companyName?: string;
  voucherSeries?: string;
  generateLedgers?: boolean;
}

class TallyXMLGenerator {
  generateXML(
    transactions: MappedTransaction[],
    options: TallyXMLOptions = {}
  ): string {
    const root = create({ version: "1.0", encoding: "UTF-8" })
      .ele("ENVELOPE")
      .ele("HEADER")
      .ele("TALLYREQUEST")
      .txt("Import Data")
      .up()
      .up()
      .ele("BODY")
      .ele("IMPORTDATA")
      .ele("REQUESTDESC")
      .ele("REPORTNAME")
      .txt("Vouchers")
      .up()
      .ele("STATICVARIABLES")
      .ele("SVCURRENTCOMPANY")
      .txt(options.companyName || "Company")
      .up()
      .up()
      .up()
      .ele("REQUESTDATA");

    // Generate ledgers first (if needed)
    if (options.generateLedgers) {
      const ledgers = this.extractUniqueLedgers(transactions);
      ledgers.forEach((ledger) => {
        this.addLedgerMaster(root, ledger);
      });
    }

    // Generate vouchers
    transactions.forEach((txn) => {
      if (txn.voucherType === "Payment") {
        this.addPaymentVoucher(root, txn);
      } else if (txn.voucherType === "Receipt") {
        this.addReceiptVoucher(root, txn);
      } else {
        this.addContraVoucher(root, txn);
      }
    });

    return root.end({ prettyPrint: true });
  }

  private addPaymentVoucher(root: any, txn: MappedTransaction): void {
    const voucher = root
      .ele("TALLYMESSAGE", { "xmlns:UDF": "TallyUDF" })
      .ele("VOUCHER", {
        REMOTEID: txn.id,
        VCHTYPE: "Payment",
        ACTION: "Create",
      })
      .ele("DATE")
      .txt(this.formatDate(txn.date))
      .up()
      .ele("VOUCHERTYPENAME")
      .txt("Payment")
      .up()
      .ele("VOUCHERNUMBER")
      .txt(txn.referenceNumber || "")
      .up()
      .ele("NARRATION")
      .txt(txn.narration)
      .up();

    // Add ledger entries
    voucher
      .ele("ALLLEDGERENTRIES.LIST")
      .ele("LEDGERNAME")
      .txt("Bank Account")
      .up()
      .ele("ISDEEMEDPOSITIVE")
      .txt("No")
      .up()
      .ele("AMOUNT")
      .txt(`-${txn.debit}`)
      .up()
      .up()
      .ele("ALLLEDGERENTRIES.LIST")
      .ele("LEDGERNAME")
      .txt(txn.ledgerName)
      .up()
      .ele("ISDEEMEDPOSITIVE")
      .txt("Yes")
      .up()
      .ele("AMOUNT")
      .txt(txn.debit)
      .up()
      .up();
  }

  private addLedgerMaster(root: any, ledgerName: string): void {
    root
      .ele("TALLYMESSAGE", { "xmlns:UDF": "TallyUDF" })
      .ele("LEDGER", {
        NAME: ledgerName,
        ACTION: "Create",
      })
      .ele("NAME")
      .txt(ledgerName)
      .up()
      .ele("PARENT")
      .txt("Sundry Debtors")
      .up()
      .ele("ISBILLWISEON")
      .txt("No")
      .up()
      .ele("ISCOSTCENTRESON")
      .txt("No")
      .up()
      .up()
      .up();
  }

  private formatDate(date: Date): string {
    return date.toISOString().split("T")[0].replace(/-/g, "");
  }
}
```

---

### 7. Excel Export Module

```typescript
// export/excel-generator.ts
import * as XLSX from "xlsx";

class ExcelGenerator {
  generate(transactions: Transaction[], options: ExcelExportOptions): Buffer {
    const workbook = XLSX.utils.book_new();

    // Sheet 1: All Transactions
    const allTxnSheet = this.createTransactionSheet(transactions);
    XLSX.utils.book_append_sheet(workbook, allTxnSheet, "All Transactions");

    // Sheet 2: Debits Only
    const debits = transactions.filter((t) => t.debit > 0);
    const debitSheet = this.createTransactionSheet(debits);
    XLSX.utils.book_append_sheet(workbook, debitSheet, "Debits");

    // Sheet 3: Credits Only
    const credits = transactions.filter((t) => t.credit > 0);
    const creditSheet = this.createTransactionSheet(credits);
    XLSX.utils.book_append_sheet(workbook, creditSheet, "Credits");

    // Sheet 4: Summary
    const summarySheet = this.createSummarySheet(transactions);
    XLSX.utils.book_append_sheet(workbook, summarySheet, "Summary");

    return XLSX.write(workbook, { type: "buffer", bookType: "xlsx" });
  }

  private createTransactionSheet(transactions: Transaction[]): XLSX.WorkSheet {
    const data = transactions.map((t) => ({
      Date: t.date.toLocaleDateString("en-IN"),
      Narration: t.narration,
      "Ref No": t.referenceNumber,
      Debit: t.debit || "",
      Credit: t.credit || "",
      Balance: t.balance,
    }));

    const worksheet = XLSX.utils.json_to_sheet(data);

    // Apply formatting
    const range = XLSX.utils.decode_range(worksheet["!ref"]!);
    for (let R = range.s.r + 1; R <= range.e.r; ++R) {
      // Format debit cells (red)
      const debitCell = XLSX.utils.encode_cell({ r: R, c: 3 });
      if (worksheet[debitCell]) {
        worksheet[debitCell].s = { font: { color: { rgb: "FF0000" } } };
      }

      // Format credit cells (green)
      const creditCell = XLSX.utils.encode_cell({ r: R, c: 4 });
      if (worksheet[creditCell]) {
        worksheet[creditCell].s = { font: { color: { rgb: "00FF00" } } };
      }
    }

    // Auto-size columns
    worksheet["!cols"] = [
      { wch: 12 }, // Date
      { wch: 50 }, // Narration
      { wch: 15 }, // Ref No
      { wch: 15 }, // Debit
      { wch: 15 }, // Credit
      { wch: 15 }, // Balance
    ];

    return worksheet;
  }
}
```

---

## 🗄️ Database Schema

```sql
-- SQLite Schema for local storage

-- User settings and preferences
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Bank templates
CREATE TABLE bank_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_name TEXT NOT NULL,
    bank_code TEXT UNIQUE NOT NULL,
    date_format TEXT,
    column_mappings TEXT,  -- JSON
    detection_patterns TEXT,  -- JSON
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Ledger mapping rules
CREATE TABLE ledger_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL,
    ledger_name TEXT NOT NULL,
    voucher_type TEXT CHECK(voucher_type IN ('Receipt', 'Payment', 'Contra')),
    priority INTEGER DEFAULT 5,
    is_regex BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    usage_count INTEGER DEFAULT 0
);

-- Conversion history
CREATE TABLE conversion_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    bank_name TEXT,
    transaction_count INTEGER,
    success_rate REAL,
    output_format TEXT,
    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_hash TEXT,  -- To prevent duplicate processing
    metadata TEXT  -- JSON with additional info
);

-- Processing errors log
CREATE TABLE error_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversion_id INTEGER,
    error_type TEXT,
    error_message TEXT,
    stack_trace TEXT,
    occurred_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversion_id) REFERENCES conversion_history(id)
);

-- Indexes for performance
CREATE INDEX idx_conversion_history_date ON conversion_history(processed_at);
CREATE INDEX idx_ledger_rules_priority ON ledger_rules(priority DESC);
CREATE INDEX idx_error_logs_conversion ON error_logs(conversion_id);
```

---

## 🧪 Testing Strategy

### Unit Tests

```typescript
// __tests__/pdf-parser.test.ts
describe("PDF Parser", () => {
  it("should detect SBI bank from PDF", async () => {
    const parser = new PDFParser("test-files/sbi-statement.pdf");
    const bank = await parser.detectBank();
    expect(bank).toBe("SBI");
  });

  it("should extract correct number of transactions", async () => {
    const parser = new PDFParser("test-files/sample-statement.pdf");
    const data = await parser.parse();
    expect(data.transactions).toHaveLength(50);
  });

  it("should handle password-protected PDFs", async () => {
    const parser = new PDFParser("test-files/protected.pdf", "password123");
    const data = await parser.parse();
    expect(data).toBeDefined();
  });
});
```

### Integration Tests

```typescript
// __tests__/integration/end-to-end.test.ts
describe("End-to-End Conversion", () => {
  it("should convert SBI statement to Tally XML", async () => {
    const inputPath = "test-files/sbi-statement.pdf";
    const outputPath = "test-output/sbi-output.xml";

    await convertPDFToTally(inputPath, outputPath);

    const xmlContent = await fs.readFile(outputPath, "utf-8");
    expect(xmlContent).toContain("<ENVELOPE>");
    expect(xmlContent).toContain("<VOUCHER");
  });
});
```

---

## 🚀 Deployment Guide

### Building for Production

```bash
# Build frontend
npm run build

# Build Electron app
npm run build:electron

# Package for Windows
npm run package:win

# Package for macOS
npm run package:mac

# Package for Linux
npm run package:linux
```

### Release Checklist

- [ ] All tests passing
- [ ] Version number updated
- [ [ Documentation updated
- [ ] Changelog generated
- [ ] Build artifacts created
- [ ] Code signed (Windows/Mac)
- [ ] Installer tested
- [ ] Auto-update configured

---

**Last Updated**: December 2025  
**Version**: 1.0.0  
**Maintainer**: Developer Team
