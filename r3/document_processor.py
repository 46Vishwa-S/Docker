
# ===================================
# FILE 2: document_processor.py
# Document Processing and Hashing
# ===================================

import hashlib
import os
from pathlib import Path
from typing import Optional

class DocumentProcessor:
    """Handle document file operations and hashing"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def compute_file_hash(file_path: str) -> str:
        """Compute SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    @staticmethod
    def validate_file(file_path: str) -> tuple[bool, str]:
        """Validate file extension and size"""
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, "File does not exist"
        
        # Check extension
        if path.suffix.lower() not in DocumentProcessor.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(DocumentProcessor.ALLOWED_EXTENSIONS)}"
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > DocumentProcessor.MAX_FILE_SIZE:
            return False, f"File too large. Maximum size: {DocumentProcessor.MAX_FILE_SIZE / (1024*1024)}MB"
        
        return True, "Valid"
    
    @staticmethod
    def save_document(file_path: str, storage_dir: str = "documents") -> str:
        """Save document to storage directory"""
        os.makedirs(storage_dir, exist_ok=True)
        
        path = Path(file_path)
        file_hash = DocumentProcessor.compute_file_hash(file_path)
        
        # Save with hash as filename to prevent duplicates
        new_filename = f"{file_hash}{path.suffix}"
        new_path = os.path.join(storage_dir, new_filename)
        
        # Copy file if it doesn't exist
        if not os.path.exists(new_path):
            import shutil
            shutil.copy2(file_path, new_path)
        
        return new_path

