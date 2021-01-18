import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from transaction.Transaction import Transaction
from transaction.Payment import Payment
from transaction.Contract import Contract
from transaction.Acusation import Acusation
from wallet.Wallet import Wallet
from bit import PrivateKey, PrivateKeyTestnet, verify_sig

import pytest

# Initializing wallet so we can have a testing public and private key
wallet = Wallet()

def test_payment():
    blockchain = Blockchain(False)

    sender = wallet.public_key
    fee = 3
    amount = 1
    receiver = "<receiver>"

    transaction = Payment(sender, fee, amount, receiver)
    signature = wallet.sign_transaction(transaction)

    assert transaction.is_valid(blockchain) == False

    fee = -3

    transaction = Payment(sender, fee, amount, receiver)
    signature = wallet.sign_transaction(transaction)

    assert transaction.is_valid(blockchain) == False

    fee = 0
    amount = -1

    transaction = Payment(sender, fee, amount, receiver)
    signature = wallet.sign_transaction(transaction)

    assert transaction.is_valid(blockchain) == False

    with pytest.raises(Exception) as e:
        blockchain.add_transaction(transaction)

    assert str(e.value) == "Transaction is invalid"

    receiver = "<my_other_wallet>"

    transaction = Payment(sender, fee, amount, receiver)
    transaction.sign(signature)

    with pytest.raises(Exception) as e:
        blockchain.add_transaction(transaction)

    assert str(e.value) == "Transaction is invalid"

    fee = 0
    amount = 0
    receiver = "<receiver>"

    transaction = Payment(sender, fee, amount, receiver)
    signature = wallet.sign_transaction(transaction)

    assert transaction.is_valid(blockchain) == True

def test_contract():
    """Testing if contract transactions are working"""

    blockchain = Blockchain(False)

    sender = wallet.public_key
    fee = 0
    content = ["You shall not kill"]

    transaction = Contract(sender, fee, content)
    signature = wallet.sign_transaction(transaction)
    assert transaction.is_valid(blockchain) == True

    transaction.sign_contract(wallet.private_key)
    signature = wallet.sign_transaction(transaction)
    assert transaction.is_valid(blockchain) == True
    assert len(transaction.contract_signatures) > 0
    assert transaction.verify_signature(wallet.public_key) == True

    wallet2 = Wallet()
    assert transaction.verify_signature(wallet2.public_key) == False

    fee = 1
    transaction = Contract(sender, fee, content)
    signature = wallet.sign_transaction(transaction)
    assert transaction.is_valid(blockchain) == False

    fee = -1
    transaction = Contract(sender, fee, content)
    signature = wallet.sign_transaction(transaction)
    assert transaction.is_valid(blockchain) == False



def test_max_transactions():
    """Tesing if 'Transaction' method 'max_transaction()' is working properly"""

    blockchain = Blockchain(False)

    expected_output = []

    sender = wallet.public_key
    fee = 3
    amount = 1
    receiver = "<receiver>"

    transaction = Payment(sender, fee, amount, receiver)
    signature = wallet.sign_transaction(transaction)

    # Adding a "malicious" transaction to the list
    blockchain.transactions.append(transaction)

    sender = wallet.public_key
    fee = 0
    amount = 0
    receiver = "<receiver>"

    transaction = Payment(sender, fee, amount, receiver)
    signature = wallet.sign_transaction(transaction)

    # Adding a real transaction to the list
    blockchain.add_transaction(transaction)
    expected_output.append(transaction)

    sender = wallet.public_key
    fee = 0
    amount = 0
    receiver = "<receiver>"

    transaction = Payment(sender, fee, amount, receiver)
    transaction.signature = signature # False signature

    # Adding another "malicious" transaction to the list
    blockchain.transactions.append(transaction)

    sender = wallet.public_key
    fee = 0
    content = ["You shall not kill"]

    transaction = Contract(sender, fee, content)
    signature = wallet.sign_transaction(transaction)

    # Adding another real transaction to the list
    blockchain.add_transaction(transaction)
    expected_output.append(transaction)

    expected_output.sort(key = lambda x : x.fee, reverse = True)

    assert Transaction.max_transactions(blockchain) == expected_output
