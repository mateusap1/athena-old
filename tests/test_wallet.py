import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract

from transaction.Transaction import Transaction
from Wallet import Wallet
from Blockchain import Blockchain


wallet = Wallet()
PUBLIC_KEY = wallet.public_key

def test_signature():
    blockchain = Blockchain(False)

    payment = Payment(PUBLIC_KEY, 13, 57, PUBLIC_KEY)
    contract = Contract(
        sender = PUBLIC_KEY, 
        fee = 13,
        fine = 100,
        rules = ["NAP"],
        judges = ["Calvin", "Luther", "Knox"],
        signatures = ["<signature />"]
    )
    accusation = Accusation(
        sender=PUBLIC_KEY,
        fee=13,
        accused="<Accused />",
        contract=contract
    )
    verdict = Verdict(
        sender=PUBLIC_KEY,
        fee=13,
        accusation=accusation,
        is_guilty=True,
        description="After carefull analysis, it became clear that the accused infriged the rules, which caused serious losses to the accuser."
    )

    transactions = [payment, contract, accusation, verdict]

    for transaction in transactions:
        wallet.sign_transaction(transaction)
        assert Wallet.verify_transaction(transaction) == True
