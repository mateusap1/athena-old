from Block import Block
from wallet.Wallet import Wallet

from bit import PrivateKey, PrivateKeyTestnet

import sys
import datetime
import binascii
import hashlib


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
        valid_types = set(("contract", "trial"))

        if not self.transaction_type in valid_types:
            return False
        
        if not isinstance(self.data, dict):
            return False
        
        if not isinstance(self.fee, dict):
            return False
        
        fee_keys = set(("value", "receipt"))
        if not all(key in self.fee for key in fee_keys):
            return False
        
        receipt_keys = set(("sender_address", "miner_address", "signature"))
        if not all(key in self.fee["receipt"] for key in receipt_keys):
            return False
        
        if not Wallet.verify_transaction(self):
            return False
        
        return True
    
    # We need to add a receipt to the transaction so we can verify later if the miner was paid (in BTC)
    @staticmethod
    def create_receipt(wif_private_key):
        priv = PrivateKey(wif_private_key)
        address = priv.address

        receipt = {
            "sender_address": address
        }

        message = str(receipt)
        signature = priv.sign(address.encode())
        receipt["signature"] = signature

        return receipt
    
    @staticmethod
    def dict_to_object(dict_version):
        return Transaction(**dict_version)
    
    @staticmethod
    def get_dict_list(transactions):
        return [transaction.get_dict() for transaction in transactions]
    
    @staticmethod
    def max_transactions(transactions):
        """Return the maximum number of valid transactions from the one with higher fees to the one with lower"""
        new_transactions = transactions.copy()
        new_transactions = list(filter(lambda x : x.is_valid(), new_transactions))
        new_transactions.sort(key = lambda x : x.fee["value"], reverse = True)
        for i, transaction in enumerate(new_transactions):
            block = Block(1, 1, new_transactions, 1, hashlib.sha256("Test".encode()).hexdigest())

            if block.is_valid():
                return new_transactions
            
            new_transactions = new_transactions[:-(i+1)]

        return new_transactions