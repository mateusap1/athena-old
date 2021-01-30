import json
import hashlib

from utils import block_utils

BLOCK_SIZE_LIMIT = 10**6 # Block limit in bytes (max of 616 transactions in avarege)

class Block(object):
    def __init__(self, index: int, timestamp: str, transactions: list, proof: int, previous_hash: str):
        self.hashing = None
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
    
    def hash(self):
        encoded_block = json.dumps(self.get_dict(), sort_keys = True).encode()

        self.hashing = hashlib.sha256(encoded_block).hexdigest()
    
    def get_dict(self):
        return {
            "hash": self.hashing,
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }
    
    @staticmethod
    def dict_to_object(dict_version):
        return Block(**dict_version)
