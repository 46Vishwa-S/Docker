# ===================================

# FILE 6: README.md

# Documentation

# ===================================

"""

# DocuChain - Blockchain Document Verification System

## Setup Instructions

### 1. Install Dependencies

```bash
pip install Flask Flask-CORS Werkzeug
```

### 2. Run the API Server

```bash
python api_server.py
```

Server will start on http://localhost:5000

### 3. Run the CLI Interface

```bash
python cli_interface.py
```

### 4. Open the HTML Frontend

Open `index.html` in your browser

## Project Structure

```
docuchain/
├── blockchain.py           # Blockchain implementation
├── document_processor.py   # Document handling
├── api_server.py          # Flask REST API
├── cli_interface.py       # Command line interface
├── index.html             # Web frontend
├── uploads/               # Temporary uploads
├── documents/             # Permanent storage
└── blockchain_data.json   # Blockchain persistence
```

## API Endpoints

### POST /api/issue

Issue a new document

- Form Data: issuer_org, doc_type, doc_title, recipient_name, recipient_id, file

### POST /api/verify

Verify a document

- Form Data: file

### GET /api/documents/<recipient_id>

Get documents for a recipient

### GET /api/documents

Get all documents

### GET /api/blockchain

Get entire blockchain

### GET /api/health

Health check

## Features

✅ SHA-256 document hashing
✅ Proof of Work blockchain
✅ Tamper-proof verification
✅ RESTful API
✅ Web interface
✅ CLI interface
✅ Persistent storage
✅ File validation

## Security Features

- Documents are hashed using SHA-256
- Blockchain uses Proof of Work mining
- Immutable record of all documents
- Tamper detection
- File size and type validation

## Usage Examples

### Issue Document (CLI)

```
1. Choose "Issue New Document"
2. Enter file path
3. Fill in document details
4. Document is hashed and added to blockchain
```

### Verify Document (CLI)

```
1. Choose "Verify Document"
2. Enter file path
3. System checks blockchain
4. Shows valid/invalid status
```

## Technologies Used

- Python 3.8+
- Flask (REST API)
- Blockchain (Custom implementation)
- SHA-256 Cryptography
- HTML/CSS/JavaScript (Frontend)

## License

MIT License
"""
