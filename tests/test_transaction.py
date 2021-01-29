import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from transaction.Transaction import Transaction
from transaction.Payment import Payment
from transaction.Contract import Contract
from transaction.Accusation import Accusation
from transaction.Defense import Defense
from transaction.Recon import Recon
from transaction.Veredict import Veredict

import pytest

PUBLIC_KEY = "30819f300d06092a864886f70d010101050003818d003081890281810098d0f0517c865e75fae9167200bb7a39c0947174467f6a0f52f715acf4103da4d1af9e51af781413ff8738435f1e4d771d24cd605149ccde2161f3d2893c2f3fa9641be3cdf45653a5c7ea02e925f1e7fad887bcde3629df5e8e7006c6c18fb212118d0665e61cf0e0ea78cb505b726ab0f8560e500c7e968a5c2baeee6713d30203010001"

def test_payment():
    blockchain = Blockchain(False)

    payment = Payment(PUBLIC_KEY, 13, 57, PUBLIC_KEY)

    assert payment.to_dict() == {
        "hash": None,
        "sender": PUBLIC_KEY,
        "signature": None,
        "amount": 57,
        "receiver": PUBLIC_KEY,
        "fee": 13
    }
    assert payment.get_content() == {
        "sender": PUBLIC_KEY,
        "amount": 57,
        "receiver": PUBLIC_KEY,
        "fee": 13
    }

def test_contract():
    """Testing if contract transactions are working"""

    blockchain = Blockchain(False)

    contract = Contract(PUBLIC_KEY, 13, ["NAP"])

    assert contract.to_dict() == {
        "hash": None,
        "sender": PUBLIC_KEY,
        "signature": None,
        "rules": ["NAP"],
        "fee": 13
    }
    assert contract.get_content() == {
        "sender": PUBLIC_KEY,
        "rules": ["NAP"],
        "fee": 13
    }

def test_recon():
    """Testing if recon transactions are working"""

    blockchain = Blockchain(False)

    contract = Contract(
        sender = PUBLIC_KEY, 
        fee = 13, 
        rules = ["NAP"]
    )

    recon = Recon(
        sender = PUBLIC_KEY, 
        fee = 13,
        receiver = "<Receiver />", # The persons public key that will be recognized
        contract = contract # The contract that both sender and receiver signed
    )

    assert recon.to_dict() == {
        "hash": None,
        "sender": PUBLIC_KEY,
        "signature": None,
        "receiver": "<Receiver />",
        "contract": contract.to_dict(),
        "fee": 13
    }
    assert recon.get_content() == {
        "sender": PUBLIC_KEY,
        "receiver": "<Receiver />",
        "contract": contract.to_dict(),
        "fee": 13
    }

def test_accusation():
    """Testing if accusation transactions are working"""

    blockchain = Blockchain(False)

    contract = Contract(
        sender = PUBLIC_KEY, 
        fee = 13, 
        rules = ["NAP"]
    )

    accusation = Accusation(
        sender = PUBLIC_KEY, 
        fee = 13, 
        accused = "<Accused />", 
        contract = contract, 
        rule_index = 17,
        proposed_fine = 100.0,
        judge = "<Judge />"
    )

    assert accusation.to_dict() == {
        "hash": None,
        "sender": PUBLIC_KEY,
        "signature": None,
        "accused": "<Accused />",
        "contract": contract.to_dict(),
        "rule_index": 17,
        "judge": "<Judge />",
        "proposed_fine": 100.0,
        "fee": 13
    }
    assert accusation.get_content() == {
        "sender": PUBLIC_KEY,
        "accused": "<Accused />",
        "contract": contract.to_dict(),
        "rule_index": 17,
        "judge": "<Judge />",
        "proposed_fine": 100.0,
        "fee": 13
    }

def test_defense():
    """Testing if defense transactions are working"""

    blockchain = Blockchain(False)

    contract = Contract(
        sender = PUBLIC_KEY, 
        fee = 13, 
        rules = ["NAP"]
    )

    accusation = Accusation(
        sender = PUBLIC_KEY, 
        fee = 13, 
        accused = "<Accused />", 
        contract = contract, 
        rule_index = 17,
        proposed_fine = 100.0,
        judge = "<Judge />"
    )

    defense = Defense(
        sender = PUBLIC_KEY, 
        fee = 13, 
        accusation = accusation,
        judge = "<Judge />"
    )

    assert defense.to_dict() == {
        "hash": None,
        "sender": PUBLIC_KEY,
        "signature": None,
        "accusation": accusation.to_dict(),
        "judge": "<Judge />",
        "fee": 13
    }
    assert defense.get_content() == {
        "sender": PUBLIC_KEY,
        "accusation": accusation.to_dict(),
        "judge": "<Judge />",
        "fee": 13
    }

def test_veredict():
    """Testing if veredict transactions are working"""

    blockchain = Blockchain(False)

    contract = Contract(
        sender = PUBLIC_KEY, 
        fee = 13, 
        rules = ["NAP"]
    )

    accusation = Accusation(
        sender = PUBLIC_KEY, 
        fee = 13, 
        accused = "<Accused />", 
        contract = contract, 
        rule_index = 17,
        proposed_fine = 100.0,
        judge = "<Judge />"
    )

    veredict = Veredict(
        sender = PUBLIC_KEY, 
        fee = 13, 
        accusation = accusation,
        is_guilty = True,
        description = "After carefull analysis, it became clear that the accused infriged the rules, which caused serious losses to the accuser."
    )

    assert veredict.to_dict() == {
        "hash": None,
        "sender": PUBLIC_KEY,
        "signature": None,
        "accusation": accusation.to_dict(),
        "is_guilty": True,
        "description": "After carefull analysis, it became clear that the accused infriged the rules, which caused serious losses to the accuser.",
        "fee": 13
    }
    
    assert veredict.get_content() == {
        "sender": PUBLIC_KEY,
        "accusation": accusation.to_dict(),
        "is_guilty": True,
        "description": "After carefull analysis, it became clear that the accused infriged the rules, which caused serious losses to the accuser.",
        "fee": 13
    }

