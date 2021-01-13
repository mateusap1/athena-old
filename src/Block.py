import json
import hashlib


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
        dict_version = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }

        return dict_version
    
    @staticmethod
    def dict_to_object(dict_version):
        return Block(**dict_version)
