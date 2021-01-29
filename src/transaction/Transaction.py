import hashlib
import json


class Transaction(object):

    def __init__(self, sender, fee):
        self.sender = sender
        self.fee = fee
        self.hashing = None
        self.signature = None
    
    def sign(self, signature):
        self.signature = signature
    
    def hash(self):
        encoded_transaction = json.dumps(self.get_content(), sort_keys = True).encode()

        self.hashing = hashlib.sha256(encoded_transaction).hexdigest()

    @staticmethod
    def dict_to_object(dict_version):
        return Transaction(**dict_version)
    
    @staticmethod
    def get_dict_list(transactions: list) -> list:
        return [transaction.get_dict() for transaction in transactions]