# Coding Standards & Project Rules

## PDF Bank Statement to Tally Converter

> **Last Updated**: December 2025  
> **Version**: 1.0  
> **Status**: Enforced

---

## 📋 Table of Contents

1. [Language-Specific Style Guides](#1-language-specific-style-guides)
2. [Project Structure](#2-project-structure)
3. [Naming Conventions](#3-naming-conventions)
4. [Linting & Formatting](#4-linting--formatting)
5. [Git Workflow](#5-git-workflow)
6. [Code Review](#6-code-review)
7. [Testing Requirements](#7-testing-requirements)
8. [CI/CD Pipeline](#8-cicd-pipeline)
9. [Dependencies & Security](#9-dependencies--security)
10. [Documentation Standards](#10-documentation-standards)
11. [File Upload Handling](#11-file-upload-handling)
12. [Performance & Accessibility](#12-performance--accessibility)
13. [Enforcement](#13-enforcement)

---

## 1. Language-Specific Style Guides

### 1.1 TypeScript/JavaScript

#### Style Guide: Airbnb + TypeScript

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript strict mode
- Prefer `const` over `let`, never use `var`
- Use arrow functions for callbacks
- Prefer template literals over string concatenation

#### Examples

**✅ Good:**

```typescript
const calculateTotal = (items: Transaction[]): number => {
  return items.reduce((sum, item) => sum + item.amount, 0);
};

const message = `Total: ${formatCurrency(total)}`;
```

**❌ Bad:**

```typescript
var calculateTotal = function (items) {
  var sum = 0;
  for (var i = 0; i < items.length; i++) {
    sum = sum + items[i].amount;
  }
  return sum;
};

var message = "Total: " + formatCurrency(total);
```

#### TypeScript Specific Rules

1. **Always specify types** - No implicit `any`

```typescript
// ✅ Good
function parseDate(dateStr: string): Date {
  return new Date(dateStr);
}

// ❌ Bad
function parseDate(dateStr) {
  return new Date(dateStr);
}
```

2. **Use interfaces for object shapes**

```typescript
// ✅ Good
interface Transaction {
  id: string;
  date: Date;
  amount: number;
  description: string;
}

// ❌ Bad
type Transaction = {
  id: any;
  date: any;
  amount: any;
  description: any;
};
```

3. **Prefer `type` for unions/primitives, `interface` for objects**

```typescript
// ✅ Good
type FileFormat = "pdf" | "csv" | "excel" | "image";
interface FileMetadata {
  name: string;
  size: number;
  format: FileFormat;
}

// ❌ Bad
interface FileFormat {
  value: string;
}
```

---

### 1.2 Python

#### Style Guide: PEP 8 + Type Hints

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Follow [PEP 484](https://peps.python.org/pep-0484/) for type hints
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use snake_case for functions and variables
- Use PascalCase for classes

#### Examples

**✅ Good:**

```python
from typing import List, Optional
from datetime import datetime

class BankStatement:
    """Represents a bank statement."""

    def __init__(self, account_number: str, statement_date: datetime) -> None:
        self.account_number = account_number
        self.statement_date = statement_date
        self._transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the statement."""
        self._transactions.append(transaction)

    def get_balance(self) -> float:
        """Calculate the total balance."""
        return sum(txn.amount for txn in self._transactions)
```

**❌ Bad:**

```python
class bankStatement:
    def __init__(self,accountNumber,statementDate):
        self.accountNumber=accountNumber
        self.statementDate=statementDate
        self.transactions=[]

    def addTransaction(self,transaction):
        self.transactions.append(transaction)

    def getBalance(self):
        total=0
        for txn in self.transactions:total+=txn.amount
        return total
```

#### Python Specific Rules

1. **Always use type hints**

```python
# ✅ Good
def parse_amount(amount_str: str) -> float:
    return float(amount_str.replace(',', ''))

# ❌ Bad
def parse_amount(amount_str):
    return float(amount_str.replace(',', ''))
```

2. **Use docstrings for all public functions/classes**

```python
# ✅ Good
def validate_iban(iban: str) -> bool:
    """
    Validate IBAN format.

    Args:
        iban: The IBAN string to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_iban("GB82WEST12345698765432")
        True
    """
    return len(iban) >= 15 and iban[:2].isalpha()

# ❌ Bad
def validate_iban(iban: str) -> bool:
    return len(iban) >= 15 and iban[:2].isalpha()
```

3. **Use context managers for resources**

```python
# ✅ Good
with open('statement.pdf', 'rb') as f:
    content = f.read()

# ❌ Bad
f = open('statement.pdf', 'rb')
content = f.read()
f.close()
```

---

## 2. Project Structure

### 2.1 Recommended Folder Structure

```
ledger-converter/
├── .agent/
│   └── workflows/
│       └── build-project.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── ci.yml
│       ├── lint.yml
│       └── deploy.yml
├── backend/
│   ├── src/
│   │   ├── services/
│   │   │   ├── TallyXMLGenerator.ts
│   │   │   ├── ExcelGenerator.ts
│   │   │   └── CSVGenerator.ts
│   │   ├── controllers/
│   │   │   └── FileProcessingController.ts
│   │   ├── utils/
│   │   │   ├── logger.ts
│   │   │   └── validators.ts
│   │   └── types/
│   │       └── index.ts
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── package.json
│   ├── tsconfig.json
│   └── jest.config.js
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Modal.tsx
│   │   │   └── layout/
│   │   │       ├── Header.tsx
│   │   │       └── Sidebar.tsx
│   │   ├── modules/
│   │   │   ├── upload/
│   │   │   │   ├── FileUploader.tsx
│   │   │   │   ├── FileQueue.tsx
│   │   │   │   └── types.ts
│   │   │   ├── preview/
│   │   │   │   └── DataPreview.tsx
│   │   │   ├── mapping/
│   │   │   │   └── LedgerMapper.tsx
│   │   │   └── export/
│   │   │       └── ExportManager.tsx
│   │   ├── stores/
│   │   │   ├── fileStore.ts
│   │   │   ├── transactionStore.ts
│   │   │   └── settingsStore.ts
│   │   ├── utils/
│   │   │   ├── formatters.ts
│   │   │   └── validators.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tests/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── python/
│   ├── pdf_processor/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── bank_detector.py
│   │   └── table_extractor.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── csv_parser.py
│   │   └── excel_parser.py
│   ├── image_processor/
│   │   ├── __init__.py
│   │   ├── ocr.py
│   │   └── preprocessor.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base_adapter.py
│   │   ├── sbi_adapter.py
│   │   ├── hdfc_adapter.py
│   │   └── ...
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py
│   ├── config/
│   │   └── bank_patterns.json
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── fixtures/
├── docs/
│   ├── api/
│   ├── user-manual.md
│   ├── architecture.md
│   └── contributing.md
├── scripts/
│   ├── setup.sh
│   └── test-import.sh
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── .pylintrc
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── CODING_STANDARDS.md
├── CHANGELOG.md
├── README.md
├── LICENSE
└── package.json
```

### 2.2 File Organization Rules

1. **One component per file** - React components should be in separate files
2. **Colocate tests** - Test files should be near the code they test
3. **Group by feature** - Use feature folders, not technical folders
4. **Index files for clean imports** - Use `index.ts` to re-export from folders

**✅ Good:**

```
modules/
  upload/
    FileUploader.tsx
    FileUploader.test.tsx
    FileQueue.tsx
    FileQueue.test.tsx
    types.ts
    index.ts  # Re-exports all components
```

**❌ Bad:**

```
components/
  FileUploader.tsx
  FileQueue.tsx
tests/
  FileUploader.test.tsx
  FileQueue.test.tsx
types/
  upload.ts
```

---

## 3. Naming Conventions

### 3.1 Files and Folders

| Type                        | Convention                    | Example                              |
| --------------------------- | ----------------------------- | ------------------------------------ |
| TypeScript React Component  | PascalCase.tsx                | `FileUploader.tsx`                   |
| TypeScript Module           | camelCase.ts                  | `fileValidator.ts`                   |
| TypeScript Type Definitions | camelCase.ts or PascalCase.ts | `types.ts`, `Transaction.ts`         |
| Python Module               | snake_case.py                 | `pdf_parser.py`                      |
| Python Test                 | test\_\*.py                   | `test_pdf_parser.py`                 |
| Config Files                | kebab-case                    | `.eslintrc.js`, `jest.config.js`     |
| Folders                     | kebab-case or snake_case      | `pdf-processor/`, `image_processor/` |

### 3.2 Variables and Functions

#### TypeScript

```typescript
// Variables: camelCase
const fileCount = 10;
const transactionList: Transaction[] = [];

// Functions: camelCase
function calculateTotal(amount: number): number {}
const processFile = (file: File): Promise<void> => {};

// Classes: PascalCase
class FileValidator {}

// Interfaces: PascalCase with 'I' prefix (optional)
interface Transaction {}
interface IFileMetadata {}

// Types: PascalCase
type FileFormat = "pdf" | "csv";

// Enums: PascalCase for enum, UPPER_CASE for values
enum FileStatus {
  PENDING = "PENDING",
  PROCESSING = "PROCESSING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED",
}

// Constants: UPPER_CASE
const MAX_FILE_SIZE = 52428800;
const SUPPORTED_FORMATS = ["pdf", "csv", "excel", "image"];
```

#### Python

```python
# Variables: snake_case
file_count = 10
transaction_list: List[Transaction] = []

# Functions: snake_case
def calculate_total(amount: float) -> float:
    pass

def process_file(file_path: str) -> None:
    pass

# Classes: PascalCase
class FileValidator:
    pass

# Constants: UPPER_CASE
MAX_FILE_SIZE = 52428800
SUPPORTED_FORMATS = ['pdf', 'csv', 'excel', 'image']

# Private members: _leading_underscore
class BankStatement:
    def __init__(self):
        self._transactions = []  # Private

    def _calculate_fee(self):  # Private method
        pass
```

### 3.3 Boolean Naming

Use prefixes that indicate boolean nature:

```typescript
// ✅ Good
const isValid = true;
const hasErrors = false;
const canSubmit = true;
const shouldRetry = false;

// ❌ Bad
const valid = true;
const errors = false;
const submit = true;
```

---

## 4. Linting & Formatting

### 4.1 ESLint Configuration

**File**: `.eslintrc.js`

```javascript
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "airbnb",
    "airbnb-typescript",
    "prettier",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: "latest",
    sourceType: "module",
    project: "./tsconfig.json",
  },
  plugins: ["react", "@typescript-eslint", "prettier"],
  rules: {
    "prettier/prettier": "error",
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "no-console": ["warn", { allow: ["warn", "error"] }],
    "max-len": [
      "error",
      { code: 100, ignoreStrings: true, ignoreTemplateLiterals: true },
    ],
  },
  settings: {
    react: {
      version: "detect",
    },
  },
};
```

### 4.2 Prettier Configuration

**File**: `.prettierrc`

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### 4.3 Python Linting (Pylint + Black)

**File**: `.pylintrc`

```ini
[MASTER]
init-hook='import sys; sys.path.append(".")'

[MESSAGES CONTROL]
disable=C0330,C0326,too-few-public-methods

[FORMAT]
max-line-length=100
indent-string='    '

[BASIC]
good-names=i,j,k,df,id,_

[DESIGN]
max-args=7
max-attributes=10
```

**File**: `pyproject.toml`

```toml
[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### 4.4 Running Linters

**Package.json scripts:**

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,json,md}\""
  }
}
```

**Python commands:**

```bash
# Lint Python code
pylint python/

# Format Python code
black python/
isort python/

# Type check
mypy python/
```

---

## 5. Git Workflow

### 5.1 Branch Naming Convention

```
<type>/<ticket-number>-<short-description>

Types:
- feature/  : New features
- fix/      : Bug fixes
- hotfix/   : Urgent production fixes
- refactor/ : Code refactoring
- docs/     : Documentation updates
- test/     : Test additions/updates
- chore/    : Maintenance tasks
```

**Examples:**

```
feature/123-add-csv-parser
fix/456-balance-calculation-error
hotfix/789-security-patch
refactor/321-simplify-upload-logic
docs/654-update-api-docs
```

### 5.2 Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance
- `ci`: CI/CD changes
- `build`: Build system changes

**Examples:**

```
feat(upload): add multi-format file validation

- Implemented validators for PDF, CSV, Excel, Images
- Added file size validation (50MB limit)
- Added MIME type checking
- Added unit tests with 95% coverage

Closes #123
```

```
fix(parser): correct balance calculation for HDFC statements

The balance calculation was incorrectly handling credit entries
for HDFC bank statements. Updated the parser to properly identify
credit vs debit columns.

Fixes #456
```

```
docs(readme): update installation instructions

Added Windows-specific setup steps and troubleshooting section.
```

### 5.3 Merge Strategy

1. **Feature branches** → `develop` : **Squash and merge**
2. **Develop** → `main` : **Merge commit**
3. **Hotfix** → `main` : **Merge commit** (then backport to develop)

### 5.4 Pull Request Rules

1. **Must pass all CI checks** before merge
2. **Requires at least 1 approval** from code owner
3. **Must be up-to-date** with target branch
4. **No direct commits to `main` or `develop`**
5. **Delete branch after merge**

---

## 6. Code Review

### 6.1 Pull Request Template

**File**: `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Description

<!-- Provide a brief description of the changes -->

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues

<!-- Link to related issues: Closes #123, Fixes #456 -->

## Changes Made

<!-- List the specific changes -->

-
-
-

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing

## Documentation

- [ ] Code documentation updated
- [ ] README updated (if applicable)
- [ ] CHANGELOG updated

## Screenshots (if applicable)

<!-- Add screenshots for UI changes -->

## Checklist

- [ ] Code follows project coding standards
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] No console errors or warnings
- [ ] Linting passes
- [ ] Tests pass
- [ ] Documentation updated
```

### 6.2 Code Review Checklist

#### Functionality

- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No security vulnerabilities introduced

#### Code Quality

- [ ] Follows coding standards
- [ ] Names are clear and descriptive
- [ ] No code duplication
- [ ] Functions are small and focused
- [ ] Complexity is manageable

#### Testing

- [ ] Unit tests cover new code
- [ ] Tests are meaningful
- [ ] Test coverage target met (>80%)
- [ ] Integration tests added if needed

#### Performance

- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No memory leaks
- [ ] File handling is efficient

#### Documentation

- [ ] Code is self-documenting or commented
- [ ] API documentation updated
- [ ] README updated if public interface changed

---

## 7. Testing Requirements

### 7.1 Testing Philosophy

**Test Pyramid:**

```
        /\
       /  \      E2E Tests (10%)
      /    \     - Full user workflows
     /------\
    /        \   Integration Tests (20%)
   /          \  - Module interactions
  /------------\
 /              \ Unit Tests (70%)
/________________\ - Individual functions
```

### 7.2 Coverage Targets

| Type              | Minimum Coverage | Target Coverage |
| ----------------- | ---------------- | --------------- |
| Unit Tests        | 80%              | 90%             |
| Integration Tests | 60%              | 75%             |
| Overall           | 75%              | 85%             |

### 7.3 Unit Testing (Jest + React Testing Library)

**File naming**: `*.test.ts`, `*.test.tsx`

**Example:**

```typescript
// FileUploader.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { FileUploader } from "./FileUploader";

describe("FileUploader", () => {
  it("should accept PDF files", () => {
    render(<FileUploader />);
    const input = screen.getByTestId("file-input");

    const file = new File(["content"], "statement.pdf", {
      type: "application/pdf",
    });
    fireEvent.change(input, { target: { files: [file] } });

    expect(screen.getByText("statement.pdf")).toBeInTheDocument();
  });

  it("should reject files over 50MB", () => {
    render(<FileUploader />);
    const input = screen.getByTestId("file-input");

    const largeFile = new File(["x".repeat(60000000)], "large.pdf", {
      type: "application/pdf",
    });
    fireEvent.change(input, { target: { files: [largeFile] } });

    expect(screen.getByText(/exceeds 50MB limit/i)).toBeInTheDocument();
  });
});
```

### 7.4 Python Testing (pytest)

**File naming**: `test_*.py`

**Example:**

```python
# test_csv_parser.py
import pytest
from parsers.csv_parser import CSVParser

class TestCSVParser:
    def test_parse_valid_csv(self):
        parser = CSVParser('fixtures/valid_statement.csv')
        df = parser.parse()

        assert len(df) > 0
        assert 'date' in df.columns
        assert 'amount' in df.columns

    def test_detect_comma_delimiter(self):
        parser = CSVParser('fixtures/comma_delimited.csv')
        delimiter = parser.detect_delimiter()

        assert delimiter == ','

    def test_reject_invalid_structure(self):
        parser = CSVParser('fixtures/invalid.csv')

        with pytest.raises(ValueError, match='Invalid CSV structure'):
            parser.validate_structure()
```

### 7.5 Test Organization

```
tests/
├── unit/
│   ├── test_file_validator.py
│   ├── test_csv_parser.py
│   └── test_pdf_reader.py
├── integration/
│   ├── test_upload_flow.py
│   └── test_export_flow.py
├── e2e/
│   └── test_complete_workflow.py
└── fixtures/
    ├── sample_statements/
    │   ├── sbi.pdf
    │   ├── hdfc.csv
    │   └── icici.xlsx
    └── expected_outputs/
        └── sbi_output.xml
```

### 7.6 Running Tests

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2"
  }
}
```

```bash
# Python tests
pytest                          # Run all tests
pytest --cov=python/ --cov-report=html  # With coverage
pytest -v                       # Verbose
pytest -k test_csv_parser       # Run specific test
```

---

## 8. CI/CD Pipeline

### 8.1 GitHub Actions Workflow

**File**: `.github/workflows/ci.yml`

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier
        run: npm run format:check

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --maxWorkers=2

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/lcov.info

  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linters
        run: |
          pylint python/
          black --check python/
          mypy python/

      - name: Run tests
        run: |
          pytest --cov=python/ --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    needs: [lint, test-frontend, test-python]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Build frontend
        run: |
          cd frontend
          npm ci
          npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-artifacts
          path: frontend/dist/
```

### 8.2 Deployment Checklist

Before deploying to production:

- [ ] All tests passing
- [ ] Code coverage targets met
- [ ] Security scan completed (no high/critical vulnerabilities)
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Release notes prepared
- [ ] Backup of current production taken
- [ ] Rollback plan ready
- [ ] Monitoring alerts configured
- [ ] Stakeholders notified

---

## 9. Dependencies & Security

### 9.1 Dependency Management

#### Adding Dependencies

1. **Check necessity** - Do we really need this package?
2. **Check license** - Is it compatible (MIT, Apache 2.0, BSD)?
3. **Check security** - Run `npm audit` or `pip-audit`
4. **Check maintenance** - Last update, issue count, stars
5. **Document reason** - Add comment in package.json

**Example:**

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "zustand": "^4.4.0", // State management - lightweight alternative to Redux
    "xlsx": "^0.18.5" // Excel file generation and parsing
  }
}
```

#### Updating Dependencies

```bash
# Check for updates
npm outdated
pip list --outdated

# Update with caution
npm update --save
pip install --upgrade packagename

# Run tests after updates
npm test
pytest
```

### 9.2 Security Policies

#### Secret Management

**✅ Do:**

- Use environment variables for secrets
- Use `.env` files (add to `.gitignore`)
- Use secret managers (AWS Secrets Manager, Azure Key Vault)
- Rotate secrets regularly

**❌ Don't:**

- Hardcode secrets in code
- Commit secrets to git
- Share secrets via email/Slack
- Log sensitive data

**Example .env:**

```env
# Database
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=secret123  # Never commit this file

# API Keys
TALLY_API_KEY=sk_live_xxxxxx
```

**.gitignore:**

```
.env
.env.local
.env.production
*.key
*.pem
secrets/
```

#### Security Scanning

```bash
# JavaScript/TypeScript
npm audit
npm audit fix

# Python
pip-audit
safety check

# Run in CI pipeline
```

---

## 10. Documentation Standards

### 10.1 README Structure

Every project/module must have a README with:

1. **Title and Description**
2. **Features**
3. **Installation**
4. **Usage** with examples
5. **Configuration**
6. **API Documentation** (if applicable)
7. **Testing**
8. **Contributing**
9. **License**

**Example:**

````markdown
# CSV Parser Module

Parse bank statement CSV files with automatic delimiter detection.

## Features

- Auto-detect delimiter (comma, semicolon, tab)
- Validate CSV structure
- Map columns to standard format

## Installation

```bash
pip install -r requirements.txt
```
````

## Usage

```python
from parsers import CSVParser

parser = CSVParser('statement.csv')
df = parser.parse()
print(df.head())
```

## API Documentation

See [API.md](./API.md) for detailed API reference.

## Testing

```bash
pytest tests/test_csv_parser.py
```

````

### 10.2 Code Comments

**When to comment:**
- Complex algorithms
- Non-obvious logic
- Workarounds for bugs
- TODO items
- Security considerations

**When NOT to comment:**
- Obvious code (let code be self-documenting)
- Commented-out code (use git history instead)

**✅ Good:**
```typescript
// Use binary search for better performance on sorted arrays O(log n)
function findTransaction(id: string, transactions: Transaction[]): Transaction | null {
  // Implementation
}

// FIXME: This is a temporary workaround for HDFC date format inconsistency
// Remove once bank updates their statement format
const dateStr = rawDate.replace(/\./g, '-');
````

**❌ Bad:**

```typescript
// This function adds two numbers
function add(a: number, b: number): number {
  return a + b; // Return the sum
}
```

### 10.3 CHANGELOG

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CSV file upload support
- Excel file upload support

## [1.0.0] - 2025-03-15

### Added

- PDF bank statement parsing
- Tally XML generation
- Excel export functionality
- Support for 10 major Indian banks

### Changed

- Improved error handling in file upload

### Fixed

- Balance calculation for HDFC statements

## [0.1.0] - 2025-02-01

### Added

- Initial project setup
- Basic PDF reader
```

---

## 11. File Upload Handling

### 11.1 Supported Formats & Specifications

| Format | Extensions              | MIME Types                                                                                      | Max Size |
| ------ | ----------------------- | ----------------------------------------------------------------------------------------------- | -------- |
| PDF    | `.pdf`                  | `application/pdf`                                                                               | 50MB     |
| Images | `.png`, `.jpg`, `.jpeg` | `image/png`, `image/jpeg`                                                                       | 50MB     |
| CSV    | `.csv`                  | `text/csv`                                                                                      | 50MB     |
| Excel  | `.xls`, `.xlsx`         | `application/vnd.ms-excel`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | 50MB     |

### 11.2 Client-Side Validation

```typescript
// frontend/src/utils/fileValidator.ts

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB in bytes

const ALLOWED_FILE_TYPES = {
  pdf: ["application/pdf"],
  image: ["image/png", "image/jpeg", "image/jpg"],
  csv: ["text/csv", "application/csv"],
  excel: [
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ],
};

const ALLOWED_EXTENSIONS = {
  pdf: [".pdf"],
  image: [".png", ".jpg", ".jpeg"],
  csv: [".csv"],
  excel: [".xls", ".xlsx"],
};

interface ValidationResult {
  valid: boolean;
  error?: string;
}

export function validateFile(file: File): ValidationResult {
  // 1. Check file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `File size (${formatBytes(file.size)}) exceeds 50MB limit`,
    };
  }

  // 2. Check file extension
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0];
  const isValidExtension = Object.values(ALLOWED_EXTENSIONS)
    .flat()
    .includes(extension || "");

  if (!isValidExtension) {
    return {
      valid: false,
      error: `Unsupported file type. Allowed: PDF, CSV, Excel, Images`,
    };
  }

  // 3. Check MIME type
  const isValidMimeType = Object.values(ALLOWED_FILE_TYPES)
    .flat()
    .includes(file.type);

  if (!isValidMimeType) {
    return {
      valid: false,
      error: `Invalid file format detected`,
    };
  }

  return { valid: true };
}

export function detectFileType(
  file: File
): "pdf" | "image" | "csv" | "excel" | "unknown" {
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0];

  if (ALLOWED_EXTENSIONS.pdf.includes(extension || "")) return "pdf";
  if (ALLOWED_EXTENSIONS.image.includes(extension || "")) return "image";
  if (ALLOWED_EXTENSIONS.csv.includes(extension || "")) return "csv";
  if (ALLOWED_EXTENSIONS.excel.includes(extension || "")) return "excel";

  return "unknown";
}
```

### 11.3 Server-Side Validation

```python
# python/utils/file_validator.py
import magic
from typing import Tuple
from pathlib import Path

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

ALLOWED_MIME_TYPES = {
    'application/pdf',
    'image/png',
    'image/jpeg',
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}

ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.csv', '.xls', '.xlsx'}

def validate_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate uploaded file on server side.

    Args:
        file_path: Path to uploaded file

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)

    # 1. Check file exists
    if not path.exists():
        return False, "File not found"

    # 2. Check file size
    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        return False, f"File size ({file_size} bytes) exceeds 50MB limit"

    # 3. Check extension
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file extension: {path.suffix}"

    # 4. Check actual file content (magic bytes)
    mime = magic.from_file(file_path, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        return False, f"Invalid file type detected: {mime}"

    # 5. Additional security checks
    if not is_safe_filename(path.name):
        return False, "Unsafe filename detected"

    return True, ""

def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe (no path traversal)."""
    return '..' not in filename and '/' not in filename and '\\' not in filename
```

### 11.4 Drag-and-Drop Behavior

```typescript
// frontend/src/modules/upload/FileUploader.tsx
import { useDropzone } from "react-dropzone";

export function FileUploader() {
  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
      // Handle accepted files
      acceptedFiles.forEach((file) => {
        const validation = validateFile(file);
        if (validation.valid) {
          addFileToQueue(file);
        } else {
          showError(validation.error);
        }
      });

      // Handle rejected files
      rejectedFiles.forEach((rejection) => {
        const errors = rejection.errors.map((e) => e.message).join(", ");
        showError(`${rejection.file.name}: ${errors}`);
      });
    },
    []
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
      "text/csv": [".csv"],
      "application/vnd.ms-excel": [".xls"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
    },
    maxSize: MAX_FILE_SIZE,
    multiple: true, // Allow batch upload
  });

  return (
    <div
      {...getRootProps()}
      className={`dropzone ${isDragActive ? "active" : ""}`}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop files here...</p>
      ) : (
        <p>Drag and drop files here, or click to browse</p>
      )}
    </div>
  );
}
```

### 11.5 Batch Upload Handling

```typescript
// Process files sequentially to avoid overload
async function processBatchUpload(files: File[]): Promise<void> {
  const results: ProcessingResult[] = [];

  for (const file of files) {
    try {
      const result = await processFile(file);
      results.push({ file: file.name, status: "success", result });
    } catch (error) {
      results.push({
        file: file.name,
        status: "failed",
        error: error.message,
      });
    }
  }

  // Display summary
  showBatchResults(results);
}
```

---

## 12. Performance & Accessibility

### 12.1 Performance Requirements

| Metric                    | Target  | Maximum |
| ------------------------- | ------- | ------- |
| Page Load Time            | < 2s    | < 3s    |
| Time to Interactive       | < 3s    | < 5s    |
| PDF Processing (100 txns) | < 10s   | < 15s   |
| XML Generation            | < 5s    | < 8s    |
| Memory Usage              | < 500MB | < 1GB   |

### 12.2 Performance Best Practices

```typescript
// ✅ Good: Use React.memo for expensive components
const TransactionRow = React.memo(({ transaction }: Props) => {
  return <tr>{/* ... */}</tr>;
});

// ✅ Good: Virtualize long lists
import { FixedSizeList } from "react-window";

function TransactionList({ transactions }: Props) {
  return (
    <FixedSizeList height={600} itemCount={transactions.length} itemSize={50}>
      {({ index, style }) => (
        <div style={style}>
          <TransactionRow transaction={transactions[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}

// ✅ Good: Lazy load modules
const PreviewEditor = lazy(() => import("./modules/preview/DataPreview"));
```

### 12.3 Accessibility (WCAG 2.1 Level AA)

```typescript
// ✅ Good: Proper ARIA labels
<button
  onClick={handleUpload}
  aria-label="Upload bank statement file"
  disabled={!hasFiles}
>
  Upload
</button>

// ✅ Good: Keyboard navigation
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
  onClick={handleClick}
>
  Click me
</div>

// ✅ Good: Screen reader announcements
<div role="status" aria-live="polite" aria-atomic="true">
  {`${filesProcessed} of ${totalFiles} files processed`}
</div>
```

---

## 13. Enforcement

### 13.1 Pre-commit Hooks (Husky)

**File**: `.husky/pre-commit`

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run linters
npm run lint
npm run format:check

# Run tests
npm test

# Python checks
pylint python/
black --check python/

# If any fail, prevent commit
```

**Installation:**

```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm run lint && npm test"
```

### 13.2 IDE Configuration

**VSCode** `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

### 13.3 Automated Enforcement in CI

- ❌ **Block PR merge** if linting fails
- ❌ **Block PR merge** if tests fail
- ❌ **Block PR merge** if coverage drops below threshold
- ❌ **Block PR merge** if security vulnerabilities found
- ✅ **Allow merge** only when all checks pass

---

## 14. Quick Reference

### 14.1 Command Cheatsheet

```bash
# Setup
npm install
pip install -r requirements.txt

# Development
npm run dev                    # Start dev server
npm run lint                   # Lint code
npm run format                 # Format code
npm test                       # Run tests
pylint python/                 # Lint Python
pytest                         # Run Python tests

# Git
git checkout -b feature/123-description
git commit -m "feat(scope): description"
git push origin feature/123-description

# Pre-merge
npm run lint && npm test       # Verify before pushing
```

### 14.2 File Template Examples

See [templates/](./templates/) for:

- React Component Template
- Python Module Template
- Test File Template
- API Documentation Template

---

## 15. Violations and Consequences

| Violation                         | First Offense            | Repeat Offense  |
| --------------------------------- | ------------------------ | --------------- |
| Committed without linting         | Warning + fix required   | PR rejected     |
| Committed without tests           | Warning + tests required | PR rejected     |
| Hardcoded secrets                 | Immediate rollback       | Security review |
| Ignored security vulnerability    | Fix within 24h           | Escalation      |
| Breaking changes without approval | Revert + discussion      | Process review  |

---

## 16. Updates to This Document

- **Suggest changes via PR** to this document
- **Review quarterly** (January, April, July, October)
- **Announce updates** in team meetings and Slack
- **Version this document** in CHANGELOG

---

**Last Reviewed**: December 2025  
**Next Review**: March 2026  
**Document Owner**: Development Team  
**Status**: ✅ Active & Enforced
