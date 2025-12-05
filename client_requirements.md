# Client Requirements Document

## PDF Bank Statement to Tally XML/Excel Converter

---

## 📋 Executive Summary

This document outlines the functional and non-functional requirements for a free alternative to Repotic's bank statement conversion service. The application must convert bank statements from multiple formats (PDF, images, CSV, Excel) into Tally XML and Excel formats with high accuracy and ease of use.

---

## 👤 Client Profile

**Name**: Your Brother  
**Current Solution**: Repotic (Paid Service)  
**Pain Points**:

- Limited conversions per month
- Subscription costs adding up
- Need for unlimited usage
- Requires multiple bank support

**Primary Use Case**: Converting bank statements for accounting and Tally entry on a regular basis (daily/weekly)

---

## 🎯 Business Requirements

### BR-1: Cost Elimination

**Priority**: Critical  
**Description**: The solution must be completely free with no usage limits, eliminating the need for paid services like Repotic.

### BR-2: Unlimited Conversions

**Priority**: Critical  
**Description**: Users should be able to convert unlimited number of bank statements without any restrictions or quotas.

### BR-3: Time Savings

**Priority**: High  
**Description**: Reduce the time spent on manual data entry from hours to minutes.

### BR-4: Accuracy Improvement

**Priority**: High  
**Description**: Minimize human errors in data entry through automated extraction with 95%+ accuracy.

### BR-5: Multiple Bank Support

**Priority**: High  
**Description**: Support bank statements from all major Indian banks without requiring separate configurations.

---

## ⚙️ Functional Requirements

### FR-1: File Upload & Management

#### FR-1.1: File Upload (Multi-Format Support)

- **Must Support**:
  - **Upload Methods:**
    - Drag and drop functionality
    - Browse and select files
    - Multiple file selection (batch upload)
  - **Supported Formats:**
    - PDF documents (`.pdf`)
    - Images (`.png`, `.jpg`, `.jpeg`) - for scanned statements
    - CSV files (`.csv`) - for direct data import
    - Excel files (`.xls`, `.xlsx`) - for spreadsheet imports
  - **File Size Limit:**
    - Up to 50MB per individual file
    - No limit on total batch size (memory permitting)
  - **Format Validation:**
    - Auto-detect file type by extension and MIME type
    - Validate file integrity before processing
    - Display clear error messages for unsupported formats

#### FR-1.2: Password-Protected PDFs

- Detect if PDF is password protected
- Prompt user to enter password
- Support common bank password formats:
  - **HDFC**: Customer ID (CIF Number)
  - **SBI**: 11-digit account number
  - **ICICI**: First 4 letters of name + DDMM (DOB)
  - **Axis**: First 4 letters of name + Last 4 digits of account
  - **Kotak**: CRN Number
  - **IndusInd**: First 4 letters + DDMM (DOB)
- Auto-unlock if password format is predictable
- Option to save passwords for future use (encrypted)

#### FR-1.3: File Queue Management

- Display list of uploaded files
- Show processing status (Pending, Processing, Completed, Failed)
- Allow file removal before processing
- Support reprocessing failed files

---

### FR-2: Bank Detection & Format Recognition

#### FR-2.1: Automatic Bank Detection

- Identify bank from file metadata (PDF, CSV, Excel headers)
- Recognize bank from logo/header (PDF, images)
- Detect bank from IFSC code or account format
- Parse bank identifier from CSV/Excel column headers
- Fallback: Manual bank selection by user

#### FR-2.2: Supported Banks (Phase 1)

Must support these major Indian banks:

1. State Bank of India (SBI)
2. HDFC Bank
3. ICICI Bank
4. Axis Bank
5. Kotak Mahindra Bank
6. Punjab National Bank (PNB)
7. Bank of Baroda (BOB)
8. Canara Bank
9. Union Bank of India
10. IndusInd Bank

#### FR-2.3: Statement Format Variations

- Support different statement layouts (detailed, mini, custom)
- Handle multi-page statements
- Process both digital and scanned (OCR) PDFs
- Recognize different date formats (DD/MM/YYYY, DD-MM-YY, etc.)

---

### FR-3: Data Extraction

#### FR-3.1: Transaction Data Fields

Extract the following mandatory fields:

- ✅ Transaction Date
- ✅ Value Date (if available)
- ✅ Description/Narration
- ✅ Cheque/Reference Number
- ✅ Debit Amount
- ✅ Credit Amount
- ✅ Balance
- ✅ Transaction Type (auto-detect)

#### FR-3.2: Account Information

Extract from statement header:

- Account holder name
- Account number
- Bank name and branch
- IFSC code
- Statement period (From Date - To Date)
- Opening balance
- Closing balance

#### FR-3.3: Data Validation

- Verify mathematical accuracy (balance calculation)
- Flag missing or suspicious entries
- Check date sequence
- Validate amount formats
- Identify duplicate transactions

---

### FR-4: Data Preview & Editing

#### FR-4.1: Preview Interface

- Display extracted data in tabular format
- Show all transactions with editable fields
- Highlight potential errors or warnings
- Display summary (total debits, credits, count)

#### FR-4.2: Manual Editing

- Allow editing of any field
- Add missing transactions manually
- Delete incorrect entries
- Merge split transactions
- Edit narration/description

#### FR-4.3: Data Corrections

- Flag and highlight errors automatically
- Suggest corrections based on patterns
- Allow bulk find-and-replace
- Undo/Redo functionality

---

### FR-5: Ledger Mapping

#### FR-5.1: Auto Ledger Mapping

- Map common transaction types to standard ledgers:
  - Salary credits → Salary Income
  - ATM withdrawals → Cash Withdrawal
  - Credit card payments → Credit Card A/c
  - UPI payments → Auto-detect based on narration
  - Bank charges → Bank Charges
  - Interest credited → Interest Income

#### FR-5.2: Custom Ledger Mapping

- Create custom mapping rules
- Save mapping templates for future use
- Import existing Tally ledger names
- Set default ledgers for unknown transactions

#### FR-5.3: Smart Categorization

- Learn from user corrections
- Suggest ledgers based on narration keywords
- Support regex-based rules
- Handle vendor/customer name matching

---

### FR-6: Output Generation

#### FR-6.1: Tally XML Export

- Generate Tally-compatible XML format
- Support Tally.ERP 9 and Tally Prime
- Include all mandatory Tally fields:
  - Voucher Date
  - Voucher Type (Receipt, Payment, Contra)
  - Ledger Name
  - Amount
  - Narration
  - Bank Name
- Create separate XML files for:
  - Receipt vouchers (Credits)
  - Payment vouchers (Debits)
  - Contra vouchers (internal transfers)

#### FR-6.2: Excel Export

- Export to .xlsx format
- Multiple sheet options:
  - **Sheet 1**: All transactions
  - **Sheet 2**: Only debits
  - **Sheet 3**: Only credits
  - **Sheet 4**: Summary
- Include formulas for totals
- Apply conditional formatting (credits in green, debits in red)
- Add filters and sorting options

#### FR-6.3: CSV Export

- Simple comma-separated format
- Compatible with other accounting software
- Include all extracted fields
- Option to customize column order

#### FR-6.4: Export Options

- Choose voucher date: Transaction date or Value date
- Include/exclude bank charges
- Merge similar transactions
- Set decimal precision
- Add custom prefix/suffix to narration

---

### FR-7: Batch Processing

#### FR-7.1: Multi-File Processing

- Upload multiple PDF statements at once
- Process all files sequentially or in parallel
- Display progress for each file
- Generate combined output or separate files

#### FR-7.2: Scheduled Processing

- Set up automatic processing of files in a folder
- Watch folder for new PDFs
- Auto-process and save to designated output folder

---

### FR-8: Templates & Configurations

#### FR-8.1: Bank Templates

- Pre-configured templates for all supported banks
- User can create custom templates for new banks
- Export/Import templates
- Template version management

#### FR-8.2: User Preferences

- Save default settings:
  - Preferred output format
  - Default ledger mappings
  - Date format preferences
  - Export location
- Multiple user profiles support

---

### FR-9: Reports & Analytics

#### FR-9.1: Conversion Summary

- Total transactions processed
- Success rate
- Errors detected and fixed
- Processing time
- File size processed

#### FR-9.2: Transaction Analytics

- Monthly/Quarterly summary
- Category-wise breakdown
- Largest transactions
- Recurring payments identification
- Cash flow visualization

---

## 🎨 User Interface Requirements

### UI-1: Dashboard

- Clean, modern interface
- Quick access to main functions
- Recent conversions history
- Statistics and usage metrics

### UI-2: Conversion Wizard

- Step-by-step guided process:
  1. Upload PDF
  2. Select Bank (if not auto-detected)
  3. Preview & Edit Data
  4. Configure Output
  5. Generate & Download
- Progress indicator
- Back/Next navigation
- Cancel option at any stage

### UI-3: Data Grid

- Sortable columns
- Filterable data
- Inline editing
- Pagination for large datasets
- Export grid view to Excel

### UI-4: Settings Panel

- Organized in tabs/sections
- Search functionality for settings
- Reset to defaults option
- Import/Export settings

---

## 🚀 Performance Requirements

### PF-1: Processing Speed

- Extract data from 100 transactions in < 10 seconds
- Complete PDF processing (500 transactions) in < 30 seconds
- Generate XML/Excel output in < 5 seconds

### PF-2: Accuracy

- Data extraction accuracy: Minimum 95%
- Balance matching accuracy: 99%+
- Date parsing accuracy: 100%

### PF-3: Resource Usage

- Application size: < 200MB installed
- RAM usage: < 500MB during processing
- Minimal CPU usage when idle

---

## 🔒 Security Requirements

### SE-1: Data Privacy

- All processing done locally (offline mode)
- No data transmitted to external servers
- Temporary files deleted after processing
- Encrypted storage of saved passwords

### SE-2: File Security

- Validate PDF integrity before processing
- Prevent malicious file execution
- Secure password handling
- No data logging or tracking

---

## 🌐 Compatibility Requirements

### CO-1: Operating Systems

- Windows 10/11 (64-bit)
- macOS 10.14+
- Linux (Ubuntu 20.04+, Fedora, Arch)

### CO-2: Tally Versions

- Tally.ERP 9 (Release 6.0 and above)
- Tally Prime (All versions)
- Tally 7.2 (optional support)

### CO-3: File Formats

- Input: PDF (1.4 to 2.0), Images (PNG, JPG, JPEG), CSV, Excel (XLS, XLSX)
- Output: XML, XLSX, CSV, JSON

---

## 📱 Accessibility Requirements

### AC-1: User Friendliness

- No technical knowledge required
- Clear error messages
- Help tooltips and guides
- Video tutorial integration

### AC-2: Localization

- English language (Phase 1)
- Hindi language support (Phase 2)
- Regional language support (Future)

---

## 🆘 Support Requirements

### SP-1: Documentation

- User manual (PDF + Online)
- Video tutorials (YouTube)
- FAQ section
- Troubleshooting guide

### SP-2: Updates

- Automatic update notifications
- One-click update installation
- Rollback to previous version option
- Change log accessible in app

### SP-3: Help System

- In-app help documentation
- Searchable help content
- Context-sensitive help
- Sample files for testing

---

## ✅ Acceptance Criteria

The application will be considered acceptable when:

1. ✅ Successfully converts PDFs from all 10 supported banks
2. ✅ Achieves 95%+ accuracy in data extraction
3. ✅ Generates valid Tally XML files that import without errors
4. ✅ Processes 500 transactions in under 30 seconds
5. ✅ Provides editable preview before export
6. ✅ Handles password-protected PDFs correctly
7. ✅ Works offline without internet connection
8. ✅ Saves 80%+ time compared to manual entry
9. ✅ Easy to use by non-technical users
10. ✅ No crashes or data loss during operation

---

## 🔄 Change Management

### Version 1.0 (MVP)

- Core functionality as described above
- Top 10 banks support
- Basic UI

### Version 1.1 (Enhancement)

- Additional 10 banks
- Advanced ledger mapping
- Improved UI/UX

### Version 2.0 (Advanced)

- OCR for scanned PDFs
- AI-based categorization
- Cloud sync option

---

## 📞 Client Sign-off

**Prepared By**: Developer (You)  
**Reviewed By**: Client (Your Brother)  
**Date**: December 2025  
**Status**: Pending Approval

**Notes**: This document should be reviewed with the client to ensure all requirements are captured accurately. Any additional requirements should be documented in addendum.
