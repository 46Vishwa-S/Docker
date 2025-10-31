
# ===================================
# FILE 4: cli_interface.py
# Command Line Interface
# ===================================

import sys
from blockchain import DocumentBlockchain
from document_processor import DocumentProcessor

class DocumentCLI:
    """Command line interface for document operations"""
    
    def __init__(self):
        self.blockchain = DocumentBlockchain(difficulty=2)
        self.blockchain.load_from_file()
        self.processor = DocumentProcessor()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("🔐 DocuChain - Blockchain Document Verification")
        print("="*50)
        print("1. Issue New Document")
        print("2. Verify Document")
        print("3. View My Documents")
        print("4. View All Documents")
        print("5. Validate Blockchain")
        print("6. Exit")
        print("="*50)
    
    def issue_document(self):
        """Issue a new document"""
        print("\n📝 Issue New Document")
        print("-" * 50)
        
        file_path = input("Enter document file path: ").strip()
        
        # Validate file
        is_valid, message = self.processor.validate_file(file_path)
        if not is_valid:
            print(f"❌ Error: {message}")
            return
        
        # Get document details
        issuer = input("Issuer Organization: ").strip()
        doc_type = input("Document Type: ").strip()
        title = input("Document Title: ").strip()
        recipient_name = input("Recipient Name: ").strip()
        recipient_id = input("Recipient ID/Email: ").strip()
        
        # Compute hash
        print("\n⏳ Computing document hash...")
        document_hash = self.processor.compute_file_hash(file_path)
        print(f"Document Hash: {document_hash}")
        
        # Save document
        print("⏳ Saving document to storage...")
        stored_path = self.processor.save_document(file_path)
        
        # Add to blockchain
        print("⏳ Mining block and adding to blockchain...")
        document_data = {
            "type": "document",
            "document_hash": document_hash,
            "issuer": issuer,
            "doc_type": doc_type,
            "title": title,
            "recipient_name": recipient_name,
            "recipient_id": recipient_id,
            "filename": file_path.split('/')[-1]
        }
        
        result = self.blockchain.add_document(document_data)
        self.blockchain.save_to_file()
        
        print("\n✅ Document Issued Successfully!")
        print(f"Block Number: #{result['block_number']}")
        print(f"Block Hash: {result['block_hash']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Stored at: {stored_path}")
    
    def verify_document(self):
        """Verify a document"""
        print("\n🔍 Verify Document")
        print("-" * 50)
        
        file_path = input("Enter document file path to verify: ").strip()
        
        if not os.path.exists(file_path):
            print("❌ Error: File does not exist")
            return
        
        # Compute hash
        print("\n⏳ Computing document hash...")
        document_hash = self.processor.compute_file_hash(file_path)
        print(f"Document Hash: {document_hash}")
        
        # Verify on blockchain
        print("⏳ Searching blockchain...")
        result = self.blockchain.verify_document(document_hash)
        
        if result:
            print("\n✅ VALID DOCUMENT - Verified on Blockchain!")
            print("-" * 50)
            print(f"Block Number: #{result['block_number']}")
            print(f"Title: {result['data']['title']}")
            print(f"Issued By: {result['data']['issuer']}")
            print(f"Recipient: {result['data']['recipient_name']}")
            print(f"Timestamp: {result['timestamp']}")
        else:
            print("\n❌ INVALID DOCUMENT")
            print("This document is NOT registered on the blockchain.")
            print("It may be counterfeit or has been tampered with.")
    
    def view_my_documents(self):
        """View documents for a recipient"""
        print("\n📄 View My Documents")
        print("-" * 50)
        
        recipient_id = input("Enter your ID/Email: ").strip()
        
        documents = self.blockchain.get_documents_by_recipient(recipient_id)
        
        if not documents:
            print(f"\n⚠️  No documents found for ID: {recipient_id}")
            return
        
        print(f"\n✅ Found {len(documents)} document(s)")
        print("=" * 50)
        
        for i, doc in enumerate(documents, 1):
            print(f"\nDocument #{i}")
            print("-" * 50)
            print(f"Title: {doc['title']}")
            print(f"Type: {doc['doc_type']}")
            print(f"Issued By: {doc['issuer']}")
            print(f"Block #: {doc['block_number']}")
            print(f"Date: {doc['timestamp']}")
            print(f"Hash: {doc['document_hash']}")
    
    def view_all_documents(self):
        """View all documents"""
        print("\n📋 All Documents in Blockchain")
        print("-" * 50)
        
        documents = self.blockchain.get_all_documents()
        
        if not documents:
            print("⚠️  No documents in blockchain yet")
            return
        
        print(f"✅ Total Documents: {len(documents)}")
        print("=" * 50)
        
        for i, doc in enumerate(documents, 1):
            print(f"\nDocument #{i}")
            print("-" * 50)
            print(f"Title: {doc['title']}")
            print(f"Recipient: {doc['recipient_name']} ({doc['recipient_id']})")
            print(f"Issued By: {doc['issuer']}")
            print(f"Block #: {doc['block_number']}")
    
    def validate_blockchain(self):
        """Validate blockchain integrity"""
        print("\n🔐 Validating Blockchain Integrity")
        print("-" * 50)
        
        is_valid = self.blockchain.is_chain_valid()
        
        if is_valid:
            print("✅ Blockchain is VALID")
            print(f"Total Blocks: {len(self.blockchain.chain)}")
        else:
            print("❌ Blockchain is INVALID - Data may have been tampered!")
    
    def run(self):
        """Run the CLI"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.issue_document()
            elif choice == '2':
                self.verify_document()
            elif choice == '3':
                self.view_my_documents()
            elif choice == '4':
                self.view_all_documents()
            elif choice == '5':
                self.validate_blockchain()
            elif choice == '6':
                print("\n👋 Thank you for using DocuChain!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    import os
    cli = DocumentCLI()
    cli.run()
