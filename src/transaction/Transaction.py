import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "../")

from Block import Block
from wallet.Wallet import Wallet

from bit import PrivateKey, PrivateKeyTestnet, verify_sig

import sys
import datetime
import binascii
import hashlib


class Transaction(object):

    def __init__(self, sender, fee):
        self.sender = sender
        self.fee = fee
        self.signature = None
    
    def sign(self, signature):
        self.signature = signature

    @staticmethod
    def dict_to_object(dict_version):
        return Transaction(**dict_version)
    
    @staticmethod
    def get_dict_list(transactions: list) -> list:
        return [transaction.get_dict() for transaction in transactions]
    
    @staticmethod
    def max_transactions(blockchain):
        """Return the maximum number of valid transactions from the one with higher fees to the one with lower"""
        new_transactions = blockchain.transactions.copy()
        new_transactions = list(filter(lambda x : x.is_valid(blockchain), new_transactions))
        new_transactions.sort(key = lambda x : x.fee, reverse = True)
        for i, transaction in enumerate(new_transactions):
            block = Block(1, 1, new_transactions, 1, hashlib.sha256("Test".encode()).hexdigest())

            if block.is_valid(blockchain):
                return new_transactions
            
            new_transactions = new_transactions[:-(i+1)]

        return new_transactions