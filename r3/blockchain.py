# ===================================
# FILE 1: blockchain.py
# Smart Contract and Blockchain Management
# ===================================

import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: str, data: Dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """Proof of Work: mine the block with given difficulty"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class DocumentBlockchain:
    """Blockchain for storing document hashes"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_documents: List[Dict] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, datetime.now().isoformat(), {
            "type": "genesis",
            "message": "Genesis Block - DocuChain System"
        }, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_document(self, document_data: Dict) -> Dict:
        """Add a new document to the blockchain"""
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=document_data,
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        return {
            "success": True,
            "block_number": new_block.index,
            "block_hash": new_block.hash,
            "timestamp": new_block.timestamp
        }
    
    def verify_document(self, document_hash: str) -> Optional[Dict]:
        """Verify if a document exists in the blockchain"""
        for block in self.chain[1:]:  # Skip genesis block
            if block.data.get("document_hash") == document_hash:
                return {
                    "valid": True,
                    "block_number": block.index,
                    "timestamp": block.timestamp,
                    "data": block.data
                }
        return None
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents from blockchain"""
        documents = []
        for block in self.chain[1:]:  # Skip genesis block
            if block.data.get("type") == "document":
                documents.append({
                    "block_number": block.index,
                    "timestamp": block.timestamp,
                    **block.data
                })
        return documents
    
    def get_documents_by_recipient(self, recipient_id: str) -> List[Dict]:
        """Get all documents for a specific recipient"""
        documents = []
        for block in self.chain[1:]:
            if block.data.get("recipient_id") == recipient_id:
                documents.append({
                    "block_number": block.index,
                    "timestamp": block.timestamp,
                    **block.data
                })
        return documents
    
    def save_to_file(self, filename: str = "blockchain_data.json"):
        """Save blockchain to file"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(filename, 'w') as f:
            json.dump(chain_data, f, indent=2)
    
    def load_from_file(self, filename: str = "blockchain_data.json"):
        """Load blockchain from file"""
        try:
            with open(filename, 'r') as f:
                chain_data = json.load(f)
            
            self.chain = []
            for block_data in chain_data:
                block = Block(
                    block_data['index'],
                    block_data['timestamp'],
                    block_data['data'],
                    block_data['previous_hash']
                )
                block.nonce = block_data['nonce']
                block.hash = block_data['hash']
                self.chain.append(block)
            
            return True
        except FileNotFoundError:
            return False






