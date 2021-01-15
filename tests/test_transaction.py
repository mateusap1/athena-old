import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from Transaction import Transaction
from wallet.Wallet import Wallet

import pytest


wallet = Wallet()

# Checking if the transaction insertion is failing when the paramaters are wrong
def test_transaction_fail_1():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    transaction_type = "Fail"
    data = {"Test": 2}
    fee = {
        "value": 3,
        "receipt": "<receipt>"
    }
    signature = wallet.sign_transaction(sender, transaction_type, data, fee)

    with pytest.raises(Exception) as e:
        blockchain.add_transaction(sender, transaction_type, data, fee, signature)

    assert str(e.value) == "Transaction type must be either \"contract\" or \"trial\""

# Checking if the transaction insertion is failing when Transaction content is altered
def test_transaction_fail_2():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    transaction_type = "contract"
    data = {"Test": 2}
    fee = {
        "value": 3,
        "receipt": "<receipt>"
    }
    signature = wallet.sign_transaction(sender, transaction_type, data, fee)
    fee["value"] = 100

    with pytest.raises(Exception) as e:
        blockchain.add_transaction(sender, transaction_type, data, fee, signature)

    assert str(e.value) == "Transaction signature does not match content"

# Checking if the transactions being inserted into the list
def test_transaction_succeed():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    transaction_types = ["contract", "trial"]
    data = {
        "content": [
            {
                "rule": "You shall not kill",
                "punishment": "Be killed"
            }
        ],
        "signatures": [
            "sfddsafsdfds234fsdf23rf"
        ]
    }
    fee = {
        "value": 3,
        "signature": "<signature>"
    }

    transactions = []
    for transaction_type in transaction_types:
        signature = wallet.sign_transaction(sender, transaction_type, data, fee)
        
        blockchain.add_transaction(sender, transaction_type, data, fee, signature)
        transactions.append(Transaction(
            sender = sender,
            transaction_type = transaction_type,
            data = data,
            fee = fee,
            signature = signature
        ).get_dict())

    assert Transaction.get_dict_list(blockchain.transactions) == transactions

def test_max_transactions_1():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    numbers = "85697"
    transaction_type = "contract"

    transactions = []

    for i in range(5):
        data = {
            "test": i
        }
        fee = {
            "value": numbers[i],
            "receipt": "<receipt>"
        }

        signature = wallet.sign_transaction(sender, transaction_type, data, fee)
        transactions.append((sender, transaction_type, data, fee, signature))

        blockchain.add_transaction(*transactions[i])

    new_transactions = Transaction.max_transactions(blockchain.transactions)
    correct_transactions = []

    transactions.sort(key = lambda x : x[3]["value"], reverse = True)
    for transaction in transactions:
        correct_transactions.append(Transaction(*transaction).get_dict())

    assert Transaction.get_dict_list(new_transactions) == correct_transactions

def test_max_transactions_2():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    numbers = "85697"
    transaction_type = "contract"

    transactions = []

    for i in range(5):
        if i == 4:
            transaction_type = "fail"

        data = {
            "test": i
        }

        fee = {
            "value": numbers[i],
            "receipt": "<receipt>"
        }

        signature = wallet.sign_transaction(sender, transaction_type, data, fee)
        transactions.append((sender, transaction_type, data, fee, signature))
        blockchain.transactions.append(Transaction(*transactions[i]))

    new_transactions = Transaction.max_transactions(blockchain.transactions)
    correct_transactions = []

    transactions.sort(key = lambda x : x[3]["value"], reverse = True)
    for transaction in transactions:
        if transaction[1] == "contract":
            correct_transactions.append(Transaction(*transaction).get_dict())

    assert Transaction.get_dict_list(new_transactions) == correct_transactions