
# ===================================
# FILE 3: api_server.py
# Flask REST API Server
# ===================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from blockchain import DocumentBlockchain
from document_processor import DocumentProcessor

app = Flask(__name__)
CORS(app)

# Initialize blockchain
blockchain = DocumentBlockchain(difficulty=2)  # Lower difficulty for faster mining
blockchain.load_from_file()

# Configuration
UPLOAD_FOLDER = 'uploads'
DOCUMENTS_FOLDER = 'documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "blockchain_length": len(blockchain.chain),
        "is_valid": blockchain.is_chain_valid()
    })


@app.route('/api/issue', methods=['POST'])
def issue_document():
    """Issue a new document"""
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get form data
        issuer_org = request.form.get('issuer_org')
        doc_type = request.form.get('doc_type')
        doc_title = request.form.get('doc_title')
        recipient_name = request.form.get('recipient_name')
        recipient_id = request.form.get('recipient_id')
        
        if not all([issuer_org, doc_type, doc_title, recipient_name, recipient_id]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Validate file
        is_valid, message = DocumentProcessor.validate_file(file_path)
        if not is_valid:
            os.remove(file_path)
            return jsonify({"error": message}), 400
        
        # Compute hash
        document_hash = DocumentProcessor.compute_file_hash(file_path)
        
        # Save to permanent storage
        stored_path = DocumentProcessor.save_document(file_path, DOCUMENTS_FOLDER)
        
        # Add to blockchain
        document_data = {
            "type": "document",
            "document_hash": document_hash,
            "issuer": issuer_org,
            "doc_type": doc_type,
            "title": doc_title,
            "recipient_name": recipient_name,
            "recipient_id": recipient_id,
            "filename": filename
        }
        
        result = blockchain.add_document(document_data)
        blockchain.save_to_file()
        
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({
            "success": True,
            "message": "Document issued successfully",
            "document_hash": document_hash,
            "block_number": result["block_number"],
            "block_hash": result["block_hash"],
            "timestamp": result["timestamp"]
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/verify', methods=['POST'])
def verify_document():
    """Verify a document"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save temporary file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Compute hash
        document_hash = DocumentProcessor.compute_file_hash(file_path)
        
        # Clean up
        os.remove(file_path)
        
        # Verify on blockchain
        result = blockchain.verify_document(document_hash)
        
        if result:
            return jsonify({
                "valid": True,
                "message": "Document is authentic and verified",
                "document_hash": document_hash,
                **result
            }), 200
        else:
            return jsonify({
                "valid": False,
                "message": "Document not found in blockchain or has been tampered",
                "document_hash": document_hash
            }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/documents/<recipient_id>', methods=['GET'])
def get_documents(recipient_id):
    """Get all documents for a recipient"""
    try:
        documents = blockchain.get_documents_by_recipient(recipient_id)
        
        return jsonify({
            "success": True,
            "count": len(documents),
            "documents": documents
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/documents', methods=['GET'])
def get_all_documents():
    """Get all documents in the blockchain"""
    try:
        documents = blockchain.get_all_documents()
        
        return jsonify({
            "success": True,
            "count": len(documents),
            "documents": documents
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """Get entire blockchain"""
    try:
        chain_data = [block.to_dict() for block in blockchain.chain]
        
        return jsonify({
            "success": True,
            "length": len(chain_data),
            "chain": chain_data,
            "is_valid": blockchain.is_chain_valid()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("DocuChain Blockchain Server Starting...")
    print("=" * 50)
    print(f"Blockchain initialized with {len(blockchain.chain)} blocks")
    print(f"API Server running on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
