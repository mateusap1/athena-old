import sys
import os
import hashlib

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from transaction.Transaction import Transaction
from wallet.Wallet import Wallet


wallet = Wallet()

def test_verify_transaction_succeed():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    transaction_type = "contract"
    data = {"Test": 2}
    fee = {
        "value": 3,
        "receipt": "<receipt>"
    }
    signature = wallet.sign_transaction(sender, transaction_type, data, fee)

    transaction = Transaction(sender, transaction_type, data, fee, signature)

    assert Wallet.verify_transaction(transaction) == True

def test_verify_transaction_fail():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    transaction_type = "contract"
    data = {"Test": 2}
    fee = {
        "value": 3,
        "receipt": "<receipt>"
    }
    signature = wallet.sign_transaction(sender, transaction_type, data, fee)
    fee = 100

    transaction = Transaction(sender, transaction_type, data, fee, signature)

    assert Wallet.verify_transaction(transaction) == False
