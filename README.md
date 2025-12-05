# Ledger - PDF Bank Statement to Tally Converter

> A free, open-source solution to convert PDF, CSV, Excel, and image bank statements into Tally XML and Excel formats.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)

---

## 📋 Overview

Ledger eliminates the need for paid services like Repotic by providing unlimited, free conversions of bank statements for seamless Tally integration. Process PDF documents, scanned images, CSV files, and Excel spreadsheets with high accuracy and zero cost.

### Key Features

- ✅ **Multi-Format Support**: PDF, Images (PNG/JPG), CSV, Excel (XLS/XLSX)
- ✅ **Smart Upload**: Drag-and-drop, batch processing, 50MB per file
- ✅ **Bank Detection**: Auto-identify from 10+ major Indian banks
- ✅ **Tally Integration**: Generate valid Tally XML for ERP 9 and Prime
- ✅ **Excel Export**: Multi-sheet exports with formulas
- ✅ **OCR Support**: Process scanned statements with Tesseract
- ✅ **Offline Processing**: All data processed locally, no cloud upload
- ✅ **Free Forever**: No usage limits, no subscriptions

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Ledger.git
cd Ledger

# Install frontend dependencies
cd frontend
npm install

# Install Python dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
```

### Run Development Server

```bash
# Frontend
cd frontend
npm run dev

# Backend (in separate terminal)
python python/main.py
```

---

## 📚 Documentation

- [User Manual](docs/user-manual.md)
- [Technical Architecture](technical_architecture.md)
- [Implementation Roadmap](implementation_roadmap.md)
- [Developer Documentation](developer_documentation.md)
- [Coding Standards](CODING_STANDARDS.md)
- [Build Workflow](.agent/workflows/build-project.md)

---

## 🏗️ Project Status

**Current Phase**: Foundation Setup  
**Version**: 0.1.0-dev  
**Status**: In Development

### Roadmap

- [x] Project documentation
- [x] Coding standards
- [x] Build workflow
- [ ] Foundation (Week 1-2)
- [ ] Core Development (Week 3-5)
- [ ] UI Development (Week 6)
- [ ] Output Generation (Week 7)
- [ ] Testing (Week 8-9)
- [ ] Documentation (Week 10)

See [implementation_roadmap.md](implementation_roadmap.md) for detailed timeline.

---

## 🏛️ Architecture

```
ledger/
├── frontend/        # React + Electron UI
├── backend/         # Node.js API layer
├── python/          # PDF/CSV/Excel processing
├── docs/            # Documentation
└── tests/           # Test suites
```

See [technical_architecture.md](technical_architecture.md) for details.

---

## 🤝 Contributing

We welcome contributions! Please follow our [Coding Standards](CODING_STANDARDS.md) and [Build Workflow](.agent/workflows/build-project.md).

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Follow coding standards
4. Write tests (80%+ coverage required)
5. Submit PR with detailed description

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built as a free alternative to Repotic
- Inspired by the need for unlimited bank statement conversions
- Thanks to all contributors and users

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Ledger/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/Ledger/wiki)
- **Email**: support@ledgerconverter.com

---

**Made with ❤️ for the accounting community**
