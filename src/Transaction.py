from Block import Block

import sys
import datetime
import binascii


class Transaction(object):

    def __init__(self, sender, transaction_type, data, fee, signature):
        self.sender = sender
        self.transaction_type = transaction_type
        self.data = data
        self.fee = fee
        self.signature = signature
    
    def get_dict(self):
        return {
            "sender": self.sender,
            "transaction_type": self.transaction_type,
            "data": self.data,
            "fee": self.fee,
            "signature": self.signature
        }
    
    def is_valid(self):
        valid_types = ["contract", "trial"]

        if not self.transaction_type in valid_types:
            return False
        
        if not isinstance(self.data, dict):
            return False
        
        return True
    
    @staticmethod
    def dict_to_object(dict_version):
        return Transaction(**dict_version)
    
    @staticmethod
    def get_dict_list(transactions):
        return [transaction.get_dict() for transaction in transactions]
    
    @staticmethod
    def max_transactions(transactions):
        """Return the maximum number of possible transactions"""
        new_transactions = transactions.copy()
        new_transactions = list(filter(lambda x : x.is_valid(), new_transactions))
        new_transactions.sort(key = lambda x : x.fee["value"], reverse = True)
        for i, transaction in enumerate(new_transactions):
            block = Block(1, 1, new_transactions, 1, 1)

            if block.is_valid():
                return new_transactions
            
            new_transactions = new_transactions[:-(i+1)]

        return new_transactions