import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create the genesis block
        self.create_block(previous_hash='1')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'previous_hash': previous_hash,
        }
        block['hash'] = self.hash(block)
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount, description):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'description': description,
            'timestamp': time()
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr['previous_hash'] != prev['hash']:
                return False
            if curr['hash'] != self.hash(curr):
                return False
        return True

# Example CLI usage
if __name__ == "__main__":
    blockchain = Blockchain()

    while True:
        print("\n--- Blockchain Transaction System ---")
        print("1. Add Transaction")
        print("2. Mine Block")
        print("3. View Blockchain")
        print("4. Check Validity")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            sender = input("Sender: ")
            receiver = input("Receiver: ")
            amount = float(input("Amount: "))
            desc = input("Description: ")
            blockchain.add_transaction(sender, receiver, amount, desc)
            print("Transaction will be added in the next block.")

        elif choice == '2':
            block = blockchain.create_block(blockchain.last_block['hash'])
            print(f"Block #{block['index']} mined!")
            print(json.dumps(block, indent=4))

        elif choice == '3':
            for blk in blockchain.chain:
                print(json.dumps(blk, indent=4))

        elif choice == '4':
            valid = blockchain.is_chain_valid()
            print("Blockchain is valid!" if valid else "Blockchain has been tampered!")

        elif choice == '5':
            break

        else:
            print("Invalid option. Try again.")