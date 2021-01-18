import json
import hashlib

from utils import block_utils

BLOCK_SIZE_LIMIT = 10**6 # Block limit in bytes (max of 616 transactions in avarege)

class Block(object):
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
    
    def get_hash(self):
        encoded_block = json.dumps(self.get_dict(), sort_keys = True).encode()

        return hashlib.sha256(encoded_block).hexdigest()
    
    def get_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }
    
    def is_valid(self, blockchain):
        block_size = block_utils.get_size(self)

        if block_size > BLOCK_SIZE_LIMIT:
            return False
        
        # The first transaction is the miner reward + fees
        first_transaction = self.transactions[0]
        total_amount = blockchain.get_current_reward()
        
        for transaction in self.transactions[1:]:
            if not transaction.is_valid(blockchain):
                return False

            total_amount += transaction.fee

        # If the first transaction amount wasn't the miner reward + fees the block is not valid
        if first_transaction.amount != total_amount:
            return False
        
        return True
    
    @staticmethod
    def dict_to_object(dict_version):
        return Block(**dict_version)
