# Technical Architecture
## PDF Bank Statement to Tally XML/Excel Converter

---

## 🎯 Architecture Goals

1. **Modularity**: Components should be loosely coupled and independently testable
2. **Scalability**: Handle increasing file sizes and complexity
3. **Maintainability**: Easy to add new banks and features
4. **Performance**: Fast processing with minimal resource usage
5. **Reliability**: Robust error handling and data validation
6. **Security**: Secure handling of sensitive financial data

---

## 🏛️ System Architecture

### Architectural Style
**Layered Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (User Interface - React Components, Electron Windows)       │
└────────────────────────┬────────────────────────────────────┘
                         │ IPC / API Calls
┌────────────────────────▼────────────────────────────────────┐
│                   Application Layer                          │
│  (Business Logic - Orchestration, Validation, Mapping)       │
└────────────────────────┬────────────────────────────────────┘
                         │ Data Flow
┌────────────────────────▼────────────────────────────────────┐
│                   Service Layer                              │
│  (Core Services - PDF Processing, Data Transformation)       │
└────────────────────────┬────────────────────────────────────┘
                         │ Data Access
┌────────────────────────▼────────────────────────────────────┐
│                   Data Layer                                 │
│  (Storage - SQLite, File System, Configuration)              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                         Frontend (Electron/React)             │
│                                                               │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Upload    │  │  Preview   │  │  Mapping │  │ Export  │ │
│  │  Component │  │  Editor    │  │  Manager │  │ Manager │ │
│  └─────┬──────┘  └──────┬─────┘  └────┬─────┘  └────┬────┘ │
│        │                 │             │             │      │
│  ┌─────▼─────────────────▼─────────────▼─────────────▼────┐ │
│  │              State Management (Zustand)                 │ │
│  └────────────────────────────┬─────────────────────────────┘ │
└────────────────────────────────┼──────────────────────────────┘
                                 │ IPC Communication
┌────────────────────────────────▼──────────────────────────────┐
│                      Main Process (Node.js)                    │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  File        │  │  Processing  │  │  Configuration    │  │
│  │  Manager     │  │  Orchestrator│  │  Manager          │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘  │
│         │                  │                   │             │
│  ┌──────▼──────────────────▼───────────────────▼──────────┐  │
│  │            Data Processing Pipeline                     │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │  │
│  │  │ PDF  │→ │ Parse│→ │Valid.│→ │ Map  │→ │Export│    │  │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘    │  │
│  └────────────────────────────────────────────────────────┘  │
│         │                                                     │
│  ┌──────▼─────────────────────────────────────────────────┐  │
│  │          Python Bridge (child_process)                  │  │
│  └──────┬─────────────────────────────────────────────────┘  │
└─────────┼──────────────────────────────────────────────────────┘
          │ Spawn Process
┌─────────▼──────────────────────────────────────────────────────┐
│                  PDF Processing Service (Python)                │
│                                                                 │
│  ┌────────────┐  ┌─────────────┐  ┌───────────┐              │
│  │ PDF Parser │  │   Table     │  │    OCR    │              │
│  │            │  │  Extractor  │  │  Engine   │              │
│  └────────────┘  └─────────────┘  └───────────┘              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              Bank Adapter Factory                      │    │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │    │
│  │  │ SBI  │  │ HDFC │  │ICICI │  │ Axis │  │  ...  │   │    │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘   │    │
│  └───────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    SQLite Database   │
              │  - Settings          │
              │  - Templates         │
              │  - History           │
              └──────────────────────┘
```

---

## 🔄 Data Flow Diagram

### Primary Flow: PDF to Tally XML

```
┌──────────┐
│   User   │
└────┬─────┘
     │ 1. Upload PDF
     ▼
┌─────────────────┐
│  File Uploader  │
└────┬────────────┘
     │ 2. Validate file
     ▼
┌──────────────────┐         ┌───────────────────┐
│  File Manager    │────────>│  Password Handler │
└────┬─────────────┘         └───────────────────┘
     │ 3. Queue file
     ▼
┌───────────────────┐
│  Processing       │
│  Orchestrator     │
└────┬──────────────┘
     │ 4. Send to Python
     ▼
┌──────────────────┐
│  Python Bridge   │
└────┬─────────────┘
     │ 5. Spawn process
     ▼
┌──────────────────────────────────────────┐
│         Python PDF Processor             │
│                                          │
│  ┌───────────────────────────────┐      │
│  │ 1. Read PDF                   │      │
│  └────────┬──────────────────────┘      │
│           ▼                              │
│  ┌───────────────────────────────┐      │
│  │ 2. Detect Bank                │      │
│  └────────┬──────────────────────┘      │
│           ▼                              │
│  ┌───────────────────────────────┐      │
│  │ 3. Load Bank Adapter          │      │
│  └────────┬──────────────────────┘      │
│           ▼                              │
│  ┌───────────────────────────────┐      │
│  │ 4. Extract Tables             │      │
│  └────────┬──────────────────────┘      │
│           ▼                              │
│  ┌───────────────────────────────┐      │
│  │ 5. Parse Transactions         │      │
│  └────────┬──────────────────────┘      │
│           ▼                              │
│  ┌───────────────────────────────┐      │
│  │ 6. Structure Data (JSON)      │      │
│  └────────┬──────────────────────┘      │
│           │                              │
└───────────┼──────────────────────────────┘
            │ 7. Return JSON
            ▼
┌──────────────────┐
│  Data Validator  │
└────┬─────────────┘
     │ 8. Validate & flag errors
     ▼
┌─────────────────┐
│  Preview Editor │<────── User reviews/edits
└────┬────────────┘
     │ 9. Apply corrections
     ▼
┌─────────────────┐
│  Ledger Mapper  │
└────┬────────────┘
     │ 10. Map to ledgers
     ▼
┌──────────────────┐
│  XML Generator   │
└────┬─────────────┘
     │ 11. Generate Tally XML
     ▼
┌──────────────────┐
│  File System     │
└────┬─────────────┘
     │ 12. Save to disk
     ▼
┌──────────┐
│   User   │
└──────────┘
```

---

## 🧩 Key Design Patterns

### 1. Factory Pattern (Bank Adapter Factory)

```python
class BankAdapterFactory:
    """Factory to create appropriate bank adapter"""
    
    _adapters = {
        'SBI': SBIAdapter,
        'HDFC': HDFCAdapter,
        'ICICI': ICICIAdapter,
        'AXIS': AxisAdapter,
        # ... more adapters
    }
    
    @classmethod
    def create_adapter(cls, bank_code: str) -> BankAdapter:
        adapter_class = cls._adapters.get(bank_code)
        
        if not adapter_class:
            raise ValueError(f"No adapter found for bank: {bank_code}")
        
        return adapter_class()
    
    @classmethod
    def register_adapter(cls, bank_code: str, adapter_class: Type[BankAdapter]):
        """Register a new bank adapter"""
        cls._adapters[bank_code] = adapter_class
```

### 2. Strategy Pattern (Extraction Strategies)

```python
class ExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, pdf_path: str) -> pd.DataFrame:
        pass

class PDFPlumberStrategy(ExtractionStrategy):
    def extract(self, pdf_path: str) -> pd.DataFrame:
        # Implementation using pdfplumber
        pass

class TabulaStrategy(ExtractionStrategy):
    def extract(self, pdf_path: str) -> pd.DataFrame:
        # Implementation using tabula-py
        pass

class TableExtractor:
    def __init__(self, strategy: ExtractionStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: ExtractionStrategy):
        self.strategy = strategy
    
    def extract(self, pdf_path: str) -> pd.DataFrame:
        return self.strategy.extract(pdf_path)
```

### 3. Observer Pattern (Progress Updates)

```typescript
interface ProgressObserver {
  update(progress: ProcessingProgress): void;
}

class ProcessingOrchestrator {
  private observers: ProgressObserver[] = [];
  
  subscribe(observer: ProgressObserver): void {
    this.observers.push(observer);
  }
  
  unsubscribe(observer: ProgressObserver): void {
    const index = this.observers.indexOf(observer);
    if (index > -1) {
      this.observers.splice(index, 1);
    }
  }
  
  private notify(progress: ProcessingProgress): void {
    this.observers.forEach(observer => observer.update(progress));
  }
  
  async processFile(file: File): Promise<void> {
    this.notify({ stage: 'uploading', percentage: 0 });
    // ... processing logic
    this.notify({ stage: 'parsing', percentage: 30 });
    // ... more processing
    this.notify({ stage: 'complete', percentage: 100 });
  }
}
```

### 4. Adapter Pattern (Bank Statement Formats)

Each bank has different PDF formats. The adapter pattern normalizes them:

```python
# Common interface
class BankAdapter(ABC):
    @abstractmethod
    def parse_statement(self, raw_data) -> StandardizedData:
        pass

# Bank-specific implementation
class HDFCAdapter(BankAdapter):
    def parse_statement(self, raw_data) -> StandardizedData:
        # HDFC-specific logic
        return StandardizedData(...)

# Usage
adapter = BankAdapterFactory.create_adapter('HDFC')
standardized_data = adapter.parse_statement(raw_pdf_data)
```

### 5. Builder Pattern (XML Generation)

```typescript
class TallyXMLBuilder {
  private xml: XMLDocument;
  
  constructor() {
    this.reset();
  }
  
  reset(): this {
    this.xml = create({ version: '1.0' }).ele('ENVELOPE');
    return this;
  }
  
  addHeader(company: string): this {
    this.xml.ele('HEADER')
      .ele('TALLYREQUEST').txt('Import Data').up()
      .ele('COMPANY').txt(company).up();
    return this;
  }
  
  addVoucher(voucher: Voucher): this {
    // Add voucher to XML
    return this;
  }
  
  build(): string {
    return this.xml.end({ prettyPrint: true });
  }
}

// Usage
const xml = new TallyXMLBuilder()
  .addHeader('My Company')
  .addVoucher(voucher1)
  .addVoucher(voucher2)
  .build();
```

---

## 🔌 Inter-Process Communication

### Electron IPC Architecture

```
┌────────────────────────────────────────────────────────┐
│                  Renderer Process (React)               │
│                                                          │
│  Component → ipcRenderer.invoke('process-pdf', data)    │
│                      ↓                                  │
│              Returns Promise<result>                    │
└────────────────────────┬───────────────────────────────┘
                         │ IPC Channel
┌────────────────────────▼───────────────────────────────┐
│                    Main Process (Node.js)               │
│                                                          │
│  ipcMain.handle('process-pdf', async (event, data) => { │
│    // 1. Validate request                               │
│    // 2. Call Python service                            │
│    // 3. Process result                                 │
│    // 4. Return to renderer                             │
│    return result;                                        │
│  })                                                      │
└────────────────────────┬───────────────────────────────┘
                         │ Child Process
┌────────────────────────▼───────────────────────────────┐
│               Python Service (Subprocess)               │
│                                                          │
│  Reads from stdin → Processes → Writes to stdout        │
└──────────────────────────────────────────────────────────┘
```

### IPC Message Format

```typescript
// Request from Renderer to Main
interface IPCRequest {
  id: string;
  channel: string;
  payload: any;
  timestamp: number;
}

// Response from Main to Renderer
interface IPCResponse {
  id: string;
  success: boolean;
  data?: any;
  error?: {
    code: string;
    message: string;
  };
  timestamp: number;
}

// Available IPC Channels
enum IPCChannels {
  PROCESS_PDF = 'process-pdf',
  GENERATE_XML = 'generate-xml',
  EXPORT_EXCEL = 'export-excel',
  LOAD_SETTINGS = 'load-settings',
  SAVE_SETTINGS = 'save-settings',
  GET_HISTORY = 'get-history'
}
```

---

## 🔐 Security Architecture

### Data Security Layers

```
┌───────────────────────────────────────────────────────┐
│  Layer 1: Input Validation                            │
│  - File type checking                                 │
│  - File size limits                                   │
│  - Malicious content scanning                         │
└────────────────────┬──────────────────────────────────┘
                     ▼
┌───────────────────────────────────────────────────────┐
│  Layer 2: Sandboxed Processing                        │
│  - Python runs in isolated subprocess                 │
│  - Limited file system access                         │
│  - No network access                                  │
└────────────────────┬──────────────────────────────────┘
                     ▼
┌───────────────────────────────────────────────────────┐
│  Layer 3: Data Encryption                             │
│  - Passwords encrypted at rest (AES-256)              │
│  - Secure credential storage                          │
│  - No data transmission to external servers           │
└────────────────────┬──────────────────────────────────┘
                     ▼
┌───────────────────────────────────────────────────────┐
│  Layer 4: Cleanup                                     │
│  - Temporary files deleted after processing           │
│  - Memory cleared                                     │
│  - No data logging                                    │
└───────────────────────────────────────────────────────┘
```

### Password Handling

```typescript
class SecurePasswordManager {
  private key: Buffer;
  
  constructor() {
    // Generate or load encryption key
    this.key = this.loadOrGenerateKey();
  }
  
  encrypt(password: string): string {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', this.key, iv);
    
    let encrypted = cipher.update(password, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return JSON.stringify({
      iv: iv.toString('hex'),
      data: encrypted,
      tag: authTag.toString('hex')
    });
  }
  
  decrypt(encrypted: string): string {
    const { iv, data, tag } = JSON.parse(encrypted);
    
    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      this.key,
      Buffer.from(iv, 'hex')
    );
    
    decipher.setAuthTag(Buffer.from(tag, 'hex'));
    
    let decrypted = decipher.update(data, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
}
```

---

## 📊 Performance Optimization

### Strategies

1. **Lazy Loading**
   - Load bank adapters only when needed
   - Lazy load heavy components (Preview Editor)

2. **Streaming Processing**
   - Process large PDFs in chunks
   - Stream data to avoid memory issues

3. **Caching**
   - Cache parsed bank templates
   - Cache ledger mapping rules
   - Memoize expensive computations

4. **Parallel Processing**
   - Batch file processing in parallel (worker threads)
   - Concurrent extraction of multiple pages

5. **Database Indexing**
   - Index frequently queried fields
   - Use prepared statements

### Code Example: Streaming Parser

```python
class StreamingPDFParser:
    """Process PDF in chunks to handle large files"""
    
    def __init__(self, pdf_path: str, chunk_size: int = 50):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
    
    def parse_in_chunks(self) -> Generator[List[Transaction], None, None]:
        """
        Yield chunks of transactions instead of loading all at once
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            for i in range(0, total_pages, self.chunk_size):
                chunk_pages = pdf.pages[i:i + self.chunk_size]
                transactions = []
                
                for page in chunk_pages:
                    page_transactions = self._extract_from_page(page)
                    transactions.extend(page_transactions)
                
                yield transactions
    
    def _extract_from_page(self, page) -> List[Transaction]:
        # Extract transactions from single page
        pass
```

---

## 🔄 Error Handling Architecture

### Error Categories

```typescript
enum ErrorCategory {
  FILE_ERROR = 'FILE_ERROR',           // File not found, corrupt, etc.
  PARSE_ERROR = 'PARSE_ERROR',         // PDF parsing failed
  VALIDATION_ERROR = 'VALIDATION_ERROR', // Data validation failed
  MAPPING_ERROR = 'MAPPING_ERROR',     // Ledger mapping failed
  EXPORT_ERROR = 'EXPORT_ERROR',       // XML/Excel generation failed
  SYSTEM_ERROR = 'SYSTEM_ERROR'        // Unexpected system errors
}

class ApplicationError extends Error {
  constructor(
    public category: ErrorCategory,
    public message: string,
    public recoverable: boolean = false,
    public userMessage?: string
  ) {
    super(message);
  }
}
```

### Error Recovery Flow

```
┌─────────────┐
│ Error Occurs│
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Log Error    │
└──────┬───────┘
       │
       ▼
┌──────────────────┐     ┌──────────────┐
│ Is Recoverable?  │────>│ Retry Logic  │
└──────┬───────────┘     └──────────────┘
       │ No
       ▼
┌──────────────────┐
│ Show User-       │
│ Friendly Message │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Offer Solutions: │
│ - Try Again      │
│ - Manual Edit    │
│ - Report Bug     │
└──────────────────┘
```

---

## 📈 Scalability Considerations

### Current Scale (MVP)
- Files: Up to 50MB per PDF
- Transactions: Up to 10,000 per statement
- Concurrent Files: 5 files in queue
- Users: Single user (desktop app)

### Future Scale (Phase 2)
- Files: Up to 100MB per PDF
- Transactions: Up to 50,000 per statement
- Concurrent Files: 20 files in parallel
- Users: Multiple users (cloud sync)

### Scalability Strategy

1. **Horizontal Scaling**: Worker thread pool for parallel processing
2. **Vertical Scaling**: Optimize algorithms and data structures
3. **Storage Scaling**: Implement pagination for large datasets
4. **Cloud Migration**: Optional cloud processing for very large files

---

## 🔍 Monitoring & Logging

### Logging Architecture

```typescript
enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
  FATAL = 4
}

class Logger {
  constructor(
    private level: LogLevel = LogLevel.INFO,
    private outputs: LogOutput[] = []
  ) {}
  
  log(level: LogLevel, message: string, context?: any): void {
    if (level >= this.level) {
      const logEntry = {
        timestamp: new Date(),
        level: LogLevel[level],
        message,
        context
      };
      
      this.outputs.forEach(output => output.write(logEntry));
    }
  }
  
  debug(message: string, context?: any): void {
    this.log(LogLevel.DEBUG, message, context);
  }
  
  error(message: string, error: Error): void {
    this.log(LogLevel.ERROR, message, {
      error: error.message,
      stack: error.stack
    });
  }
}

// Usage
const logger = new Logger(LogLevel.INFO, [
  new ConsoleOutput(),
  new FileOutput('./logs/app.log')
]);

logger.info('Processing PDF', { filename: 'statement.pdf' });
```

---

## 📝 Configuration Management

```typescript
interface AppConfig {
  pdf: {
    maxFileSize: number;
    tempDirectory: string;
    supportedBanks: string[];
  };
  processing: {
    parallelFiles: number;
    chunkSize: number;
    timeout: number;
  };
  output: {
    defaultFormat: 'xml' | 'excel' | 'csv';
    directory: string;
  };
  logging: {
    level: string;
    directory: string;
  };
}

class ConfigManager {
  private static instance: ConfigManager;
  private config: AppConfig;
  
  private constructor() {
    this.config = this.loadConfig();
  }
  
  static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }
  
  get(key: string): any {
    return _.get(this.config, key);
  }
  
  set(key: string, value: any): void {
    _.set(this.config, key, value);
    this.saveConfig();
  }
}
```

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Review Cycle**: Monthly