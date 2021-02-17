import json
import hashlib
import datetime

from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract
from transaction.Transaction import Transaction

from config import block_config
from utils import block_utils


MINING_DIFFICULTY = block_config["mining_difficulty"]
SIZE_LIMIT = block_config["size_limit"]


class Block(object):
    def __init__(self, index: int, transactions: list, previous_hash: str):
        self.hash_value = None
        self.nonce = None
        self.timestamp = None
        
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
    
    def hash(self):
        nonce = 0
        self.hash_value = ""
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)

        while not self.hash_value[:MINING_DIFFICULTY] == "0" * MINING_DIFFICULTY:
            nonce += 1

            if nonce > 10**6:
                self.timestamp = datetime.datetime.now(datetime.timezone.utc)
                nonce = 0

            self.nonce = nonce

            encoded_block = json.dumps(self.get_content(), sort_keys = True).encode()
            self.hash_value = hashlib.sha256(encoded_block).hexdigest()
    
    def is_valid(self):
        if len(self.transactions) > SIZE_LIMIT:
            return False

        for transaction in block.transactions:
            if transaction.is_valid() is False:
                return False
            
        encoded_block = json.dumps(block.get_content(), sort_keys = True).encode()
        current_hash = hashlib.sha256(encoded_block).hexdigest()

        if current_hash != block.hash_value:
            return False
        
        if block.hash_value[:MINING_DIFFICULTY] != "0" * MINING_DIFFICULTY:
            return False
        
        return True
    
    def to_dict(self):
        return {
            "hash": self.hash_value,
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash
        }
    
    def get_content(self):
        return {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash
        }
    
    @staticmethod
    def dict_to_object(dict_version):
        return Block(**dict_version)
