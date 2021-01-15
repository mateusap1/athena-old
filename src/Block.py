import json
import hashlib

from utils import block_utils

BLOCK_SIZE_LIMIT = 10**5 # Block limit in bytes (max of 616 transactions in avarege)

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
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }
    
    def is_valid(self):
        block_size = block_utils.get_size(self)
        
        return block_size < BLOCK_SIZE_LIMIT
    
    @staticmethod
    def dict_to_object(dict_version):
        return Block(**dict_version)
