---
description: Sequential build workflow with strict verification and commit protocol
---

# Project Build Workflow

## 🎯 Workflow Philosophy

**Build → Verify → Commit → Repeat**

This workflow enforces a strict sequential approach: implement one task completely, verify all features thoroughly, commit only after successful verification, then move to the next task. No parallel work, no shortcuts.

---

## 📋 Workflow Rules

### Golden Rules

1. ✅ **One Task at a Time**: Complete current task before starting next
2. ✅ **Verify Everything**: Test all features, not just new ones
3. ✅ **Commit Only on Success**: Never commit failing code
4. ✅ **Document Changes**: Every commit must have clear message
5. ✅ **No Skipping**: Follow sequence exactly as defined

### Prohibited Actions

- ❌ Starting next task before current is verified
- ❌ Committing without running tests
- ❌ Skipping verification steps
- ❌ Working on multiple tasks simultaneously
- ❌ Committing broken or incomplete code

---

## 🚀 Phase 1: Foundation (Week 1-2)

### Task 1.1: Initialize Project Structure

**Implement:**

```bash
# 1. Create project directory structure
mkdir -p frontend/src/{components,modules,utils,types}
mkdir -p python/{pdf_processor,adapters,utils}
mkdir -p backend/src/{services,controllers,utils}
mkdir -p tests/{unit,integration,e2e}
mkdir -p output/{xml,excel,csv}
mkdir -p temp/pdfs

# 2. Initialize frontend (React + Electron)
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install

# 3. Install Electron
npm install electron electron-builder --save-dev

# 4. Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Verify:**

```bash
# 1. Check directory structure
ls -la

# 2. Verify frontend starts
cd frontend
npm run dev
# Should open Vite dev server

# 3. Verify Python environment
python --version
pip --version
```

**Commit:**

```bash
git add .
git commit -m "feat: initialize project structure with React, Electron, and Python setup

- Created frontend with Vite + React + TypeScript
- Set up Python virtual environment
- Created directory structure for all modules
- Initialized package.json and basic configs"
```

---

### Task 1.2: Install Core Dependencies

**Implement:**

```bash
# Frontend dependencies
cd frontend
npm install tailwindcss @tailwindcss/forms postcss autoprefixer
npm install zustand react-hook-form zod
npm install react-dropzone xlsx date-fns lodash
npm install -D @types/lodash

# Python dependencies
pip install PyPDF2==4.0.0
pip install pdfplumber==0.10.3
pip install tabula-py==2.8.2
pip install pandas==2.1.0
pip install openpyxl==3.1.2
pip install Pillow==10.0.0
pip install opencv-python==4.8.0
pip install pytesseract==0.3.10
pip install python-dateutil==2.8.2
pip install pycryptodome==3.19.0

# Save Python dependencies
pip freeze > requirements.txt
```

**Verify:**

```bash
# 1. Check all packages installed
cd frontend && npm list --depth=0
cd .. && pip list

# 2. Test basic imports
python -c "import PyPDF2; import pdfplumber; import pandas; print('All imports successful')"

# 3. Verify Tailwind CSS
cd frontend
npx tailwindcss init -p
```

**Commit:**

```bash
git add .
git commit -m "feat: install all core dependencies

Frontend:
- Tailwind CSS for styling
- Zustand for state management
- React Hook Form + Zod for validation
- File upload and data processing libraries

Python:
- PDF processing (PyPDF2, pdfplumber, tabula-py)
- Data manipulation (pandas, openpyxl)
- Image processing (Pillow, OpenCV, pytesseract)
- Created requirements.txt"
```

---

### Task 1.3: Configure Development Environment

**Implement:**

```bash
# 1. Create .env file
cat > .env << EOF
NODE_ENV=development
PYTHON_PATH=./venv/bin/python
PDF_TEMP_DIR=./temp/pdfs
OUTPUT_DIR=./output
MAX_FILE_SIZE=52428800
SUPPORTED_BANKS=SBI,HDFC,ICICI,AXIS,KOTAK,PNB,BOB,CANARA,UNION,INDUSIND
LOG_LEVEL=debug
EOF

# 2. Configure TypeScript
# Update frontend/tsconfig.json with strict settings

# 3. Configure Tailwind
# Update frontend/tailwind.config.js

# 4. Create basic Electron main.js
```

**Verify:**

```bash
# 1. Verify environment variables load
cat .env

# 2. Test TypeScript compilation
cd frontend
npm run build
# Should compile without errors

# 3. Test Electron window
npm run electron
# Should open Electron window
```

**Commit:**

```bash
git add .
git commit -m "feat: configure development environment

- Created .env with all configuration variables
- Configured TypeScript with strict mode
- Set up Tailwind CSS configuration
- Created basic Electron main process
- Verified compilation and Electron startup"
```

---

## 🔨 Phase 2: Core Development (Week 3-5)

### Task 2.1: Implement PDF Reader Module

**Implement:**

```python
# python/pdf_processor/reader.py
class PDFReader:
    def __init__(self, pdf_path: str, password: str = None):
        self.pdf_path = pdf_path
        self.password = password

    def read(self) -> dict:
        # Implementation
        pass

    def is_encrypted(self) -> bool:
        # Implementation
        pass
```

**Verify:**

```bash
# 1. Run unit tests
python -m pytest tests/unit/test_pdf_reader.py -v

# 2. Test with sample PDFs
python -m pdf_processor.reader sample.pdf

# 3. Test password-protected PDF
python -m pdf_processor.reader encrypted.pdf --password "test123"

# 4. Expected output: PDF metadata and page count
```

**Commit:**

```bash
git add python/pdf_processor/reader.py tests/unit/test_pdf_reader.py
git commit -m "feat: implement PDF reader module

- Created PDFReader class with encryption detection
- Added password handling for protected PDFs
- Implemented metadata extraction
- Added unit tests with 95% coverage
- Tested with 5 different PDF versions"
```

---

### Task 2.2: Implement CSV Parser Module

**Implement:**

```python
# python/parsers/csv_parser.py
import pandas as pd

class CSVParser:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def parse(self) -> pd.DataFrame:
        # Implementation
        pass

    def detect_delimiter(self) -> str:
        # Implementation
        pass

    def validate_structure(self) -> bool:
        # Implementation
        pass
```

**Verify:**

```bash
# 1. Run unit tests
python -m pytest tests/unit/test_csv_parser.py -v

# 2. Test with sample CSV files
python -m parsers.csv_parser sample_statement.csv

# 3. Test delimiter detection
# Test with comma-separated
# Test with semicolon-separated
# Test with tab-separated

# 4. Validate parsing accuracy
# Compare parsed data with manual inspection
```

**Commit:**

```bash
git add python/parsers/csv_parser.py tests/unit/test_csv_parser.py
git commit -m "feat: implement CSV parser module

- Created CSVParser class with auto-delimiter detection
- Added structure validation for bank statement format
- Implemented header detection and column mapping
- Added unit tests with 90% coverage
- Tested with 10 different CSV formats"
```

---

### Task 2.3: Implement Excel Parser Module

**Implement:**

```python
# python/parsers/excel_parser.py
import openpyxl
import pandas as pd

class ExcelParser:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path

    def parse(self) -> pd.DataFrame:
        # Implementation
        pass

    def detect_sheet(self) -> str:
        # Implementation
        pass

    def validate_structure(self) -> bool:
        # Implementation
        pass
```

**Verify:**

```bash
# 1. Run unit tests
python -m pytest tests/unit/test_excel_parser.py -v

# 2. Test with .xls files
python -m parsers.excel_parser sample.xls

# 3. Test with .xlsx files
python -m parsers.excel_parser sample.xlsx

# 4. Test multi-sheet workbooks
python -m parsers.excel_parser multi_sheet.xlsx

# 5. Validate parsing accuracy
```

**Commit:**

```bash
git add python/parsers/excel_parser.py tests/unit/test_excel_parser.py
git commit -m "feat: implement Excel parser module

- Created ExcelParser for .xls and .xlsx files
- Added auto-detection for transaction sheet
- Implemented multi-sheet handling
- Added unit tests with 92% coverage
- Tested with 8 different Excel formats"
```

---

### Task 2.4: Implement Image OCR Module

**Implement:**

```python
# python/image_processor/ocr.py
import pytesseract
from PIL import Image
import cv2

class OCRProcessor:
    def __init__(self, image_path: str):
        self.image_path = image_path

    def preprocess_image(self) -> Image:
        # Enhancement implementation
        pass

    def extract_text(self) -> str:
        # OCR implementation
        pass

    def convert_to_pdf(self) -> str:
        # Image to PDF conversion
        pass
```

**Verify:**

```bash
# 1. Run unit tests
python -m pytest tests/unit/test_ocr.py -v

# 2. Test with clear images
python -m image_processor.ocr clear_statement.png

# 3. Test with low-quality scans
python -m image_processor.ocr blurry_scan.jpg

# 4. Test preprocessing enhancement
# Verify image quality improvements

# 5. Validate OCR accuracy
# Compare extracted text with actual content
# Target: >85% accuracy for clear images
```

**Commit:**

```bash
git add python/image_processor/ tests/unit/test_ocr.py
git commit -m "feat: implement image OCR module

- Created OCRProcessor with Tesseract integration
- Added image preprocessing (contrast, denoising)
- Implemented image-to-PDF conversion
- Added unit tests with 88% coverage
- Achieved 87% average OCR accuracy on test images"
```

---

### Task 2.5: Implement Bank Detection Module

**Implement:**

```python
# python/pdf_processor/bank_detector.py
class BankDetector:
    def __init__(self, patterns_path: str = 'config/bank_patterns.json'):
        self.patterns = self.load_patterns(patterns_path)

    def detect(self, text: str, metadata: dict) -> str:
        # Implementation
        pass

    def detect_from_pdf(self, pdf_path: str) -> str:
        # Implementation
        pass

    def detect_from_csv(self, csv_path: str) -> str:
        # Implementation
        pass
```

**Verify:**

```bash
# 1. Run unit tests
python -m pytest tests/unit/test_bank_detector.py -v

# 2. Test with SBI statement
python -m pdf_processor.bank_detector sbi_statement.pdf
# Expected: "SBI"

# 3. Test with HDFC statement
python -m pdf_processor.bank_detector hdfc_statement.pdf
# Expected: "HDFC"

# 4. Test all 10 supported banks
# Each should correctly identify bank

# 5. Test edge cases
# Generic PDF should return "UNKNOWN"
```

**Commit:**

```bash
git add python/pdf_processor/bank_detector.py config/bank_patterns.json tests/unit/test_bank_detector.py
git commit -m "feat: implement bank detection module

- Created BankDetector with pattern matching
- Added bank_patterns.json with 10 banks
- Implemented detection from PDF, CSV, Excel
- Added fallback to manual selection
- Achieved 95% detection accuracy on test data"
```

---

## 🎨 Phase 3: User Interface (Week 6)

### Task 3.1: Implement File Upload Component

**Implement:**

```typescript
// frontend/src/modules/upload/FileUploader.tsx
import { useDropzone } from 'react-dropzone';

export function FileUploader() {
  const onDrop = (files: File[]) => {
    // Implementation
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    // UI implementation
  );
}
```

**Verify:**

```bash
# 1. Run in development mode
cd frontend && npm run dev

# 2. Test drag-and-drop
# - Drag a PDF file → Should accept
# - Drag a CSV file → Should accept
# - Drag a PNG image → Should accept
# - Drag a TXT file → Should reject with error message

# 3. Test file browser
# - Click browse button
# - Select multiple files
# - Verify all files appear in queue

# 4. Test file size validation
# - Upload 30MB file → Should accept
# - Upload 60MB file → Should reject with size error

# 5. Test UI responsiveness
# - All animations smooth
# - No console errors
```

**Commit:**

```bash
git add frontend/src/modules/upload/
git commit -m "feat: implement file upload component

- Created FileUploader with drag-and-drop
- Added file type validation (PDF, CSV, Excel, Images)
- Implemented file size validation (50MB limit)
- Added multi-file selection support
- Tested with all supported formats"
```

---

### Task 3.2: Implement File Queue Management

**Implement:**

```typescript
// frontend/src/modules/upload/FileQueue.tsx
export function FileQueue() {
  // Implementation
}

// Add store
// frontend/src/stores/fileStore.ts
import { create } from "zustand";

interface FileStore {
  files: File[];
  addFiles: (files: File[]) => void;
  removeFile: (id: string) => void;
  clearQueue: () => void;
}
```

**Verify:**

```bash
# 1. Open application
npm run dev

# 2. Add files to queue
# - Add 3 PDF files
# - Verify all appear in list

# 3. Test remove functionality
# - Click remove on middle file
# - Verify only that file is removed

# 4. Test clear queue
# - Add 5 files
# - Click "Clear All"
# - Verify queue is empty

# 5. Test status display
# - Upload files
# - Verify status shows: Pending → Processing → Complete
```

**Commit:**

```bash
git add frontend/src/modules/upload/FileQueue.tsx frontend/src/stores/fileStore.ts
git commit -m "feat: implement file queue management

- Created FileQueue component with status display
- Implemented Zustand store for file state
- Added remove and clear functionality
- Added processing status tracking
- Tested with batch uploads"
```

---

## 📤 Phase 4: Output Generation (Week 7)

### Task 4.1: Implement Tally XML Generator

**Implement:**

```typescript
// backend/src/services/TallyXMLGenerator.ts
import { create } from "xmlbuilder2";

export class TallyXMLGenerator {
  generateXML(transactions: Transaction[]): string {
    // Implementation
  }

  private addLedgerMaster(root: any, ledger: string): void {
    // Implementation
  }

  private addVoucher(root: any, txn: Transaction): void {
    // Implementation
  }
}
```

**Verify:**

```bash
// turbo
# 1. Run unit tests
npm test -- TallyXMLGenerator.test.ts

# 2. Generate sample XML
node -e "const gen = require('./dist/services/TallyXMLGenerator'); console.log(gen.generateXML(sampleData));"

# 3. Validate XML structure
xmllint --noout generated.xml
# Should exit with code 0

# 4. Test import in Tally
# - Open Tally.ERP 9
# - Go to Import → Vouchers
# - Select generated XML
# - Verify successful import with no errors

# 5. Verify data accuracy in Tally
# - Check 10 sample transactions
# - Verify amounts, dates, ledgers match
```

**Commit:**

```bash
git add backend/src/services/TallyXMLGenerator.ts tests/
git commit -m "feat: implement Tally XML generator

- Created TallyXMLGenerator class
- Implemented voucher generation (Receipt, Payment, Contra)
- Added ledger master creation
- Generated valid XML tested in Tally.ERP 9
- Achieved 100% import success rate on test data"
```

---

### Task 4.2: Implement Excel Export

**Implement:**

```typescript
// backend/src/services/ExcelGenerator.ts
import * as XLSX from "xlsx";

export class ExcelGenerator {
  generate(transactions: Transaction[]): Buffer {
    // Implementation
  }

  private createTransactionSheet(data: Transaction[]): XLSX.WorkSheet {
    // Implementation
  }

  private createSummarySheet(data: Transaction[]): XLSX.WorkSheet {
    // Implementation
  }
}
```

**Verify:**

```bash
# 1. Run unit tests
npm test -- ExcelGenerator.test.ts

# 2. Generate sample Excel file
node scripts/test-excel-export.js

# 3. Open in Excel
# - Verify all 4 sheets present
# - Check formulas calculate correctly
# - Verify conditional formatting applied

# 4. Open in LibreOffice Calc
# - Verify compatibility
# - Check all features work

# 5. Verify data accuracy
# - Compare with source data
# - Check totals match
```

**Commit:**

```bash
git add backend/src/services/ExcelGenerator.ts tests/
git commit -m "feat: implement Excel export functionality

- Created ExcelGenerator with multi-sheet support
- Implemented 4 sheets: All, Debits, Credits, Summary
- Added formulas and conditional formatting
- Tested in Excel and LibreOffice
- Verified 100% data accuracy"
```

---

## 🧪 Phase 5: Testing & Verification (Week 8-9)

### Task 5.1: End-to-End Testing

**Implement:**

```bash
# Create E2E test suite
# tests/e2e/complete-workflow.test.ts
```

**Verify:**

```bash
// turbo
# 1. Run full E2E test
npm run test:e2e

# 2. Manual E2E verification
# Step 1: Upload SBI PDF statement
# Step 2: Verify bank detected as "SBI"
# Step 3: Preview extracted data
# Step 4: Verify all transactions displayed correctly
# Step 5: Generate Tally XML
# Step 6: Download and import into Tally
# Step 7: Verify import successful

# 3. Repeat for all formats
# - CSV file
# - Excel file
# - Image file

# 4. Test batch processing
# - Upload 5 mixed format files
# - Process all
# - Verify all outputs generated correctly
```

**Commit:**

```bash
git add tests/e2e/
git commit -m "test: add comprehensive E2E tests

- Created complete workflow test suite
- Tested all file formats (PDF, CSV, Excel, Image)
- Verified batch processing functionality
- Tested Tally import for all outputs
- Achieved 100% E2E test pass rate"
```

---

## 📚 Phase 6: Documentation (Week 10)

### Task 6.1: Create User Manual

**Implement:**

```bash
# Create docs/user-manual.md
```

**Verify:**

```bash
# 1. Review manual completeness
# - Installation steps complete
# - All features documented
# - Screenshots included
# - Troubleshooting section present

# 2. Test installation following manual
# - Fresh install on clean machine
# - Follow steps exactly
# - Note any missing steps

# 3. Verify all features mentioned
# - Cross-reference with feature list
# - Ensure nothing missing
```

**Commit:**

```bash
git add docs/user-manual.md docs/screenshots/
git commit -m "docs: create comprehensive user manual

- Added installation guide for all platforms
- Documented all features with screenshots
- Created troubleshooting section
- Added FAQ (25 questions)
- Verified manual with fresh install"
```

---

## 🔄 Verification Checklist (Use After Each Task)

### Code Quality

- [ ] Code compiles/runs without errors
- [ ] No linting errors
- [ ] No console warnings
- [ ] TypeScript types are correct
- [ ] Python type hints added

### Testing

- [ ] Unit tests written and passing
- [ ] Test coverage > 80%
- [ ] Integration tests passing
- [ ] Manual testing completed
- [ ] Edge cases tested

### Functionality

- [ ] Feature works as designed
- [ ] All acceptance criteria met
- [ ] No regressions in existing features
- [ ] Error handling implemented
- [ ] Logging added

### Documentation

- [ ] Code comments added
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] CHANGELOG entry added

---

## 📝 Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Formatting
- `chore`: Maintenance

**Example:**

```
feat(upload): add multi-format file validation

- Implemented validators for PDF, CSV, Excel, Images
- Added file size validation (50MB limit)
- Added MIME type checking
- Added unit tests with 95% coverage

Closes #123
```

---

## 🚨 What to Do When Verification Fails

1. **Stop Immediately**: Do not proceed to next task
2. **Identify Root Cause**: Debug the failing test/feature
3. **Fix the Issue**: Make necessary corrections
4. **Re-verify**: Run all verification steps again
5. **Only Then Commit**: Commit only after all checks pass

**Never commit failing code. Never skip verification.**

---

## 📊 Progress Tracking

After each task completion, update this checklist:

### Phase 1: Foundation

- [ ] Task 1.1: Initialize Project Structure
- [ ] Task 1.2: Install Core Dependencies
- [ ] Task 1.3: Configure Development Environment

### Phase 2: Core Development

- [ ] Task 2.1: PDF Reader Module
- [ ] Task 2.2: CSV Parser Module
- [ ] Task 2.3: Excel Parser Module
- [ ] Task 2.4: Image OCR Module
- [ ] Task 2.5: Bank Detection Module

### Phase 3: User Interface

- [ ] Task 3.1: File Upload Component
- [ ] Task 3.2: File Queue Management

### Phase 4: Output Generation

- [ ] Task 4.1: Tally XML Generator
- [ ] Task 4.2: Excel Export

### Phase 5: Testing

- [ ] Task 5.1: End-to-End Testing

### Phase 6: Documentation

- [ ] Task 6.1: User Manual

---

**Remember: Quality over Speed. Working code over fast code. Verified features over numerous features.**
