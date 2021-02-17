import sys
import os
import hashlib
import datetime
import math
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract

from transaction.Transaction import Transaction
from Wallet import Wallet
from Block import Block
from Blockchain import Blockchain


wallet = Wallet()

PRIVATE_KEY = wallet.private_key
PUBLIC_KEY = wallet.public_key

def test_create_block():
    blockchain = Blockchain(False)

    block = blockchain.create_block()

    assert block.hash_value[:5] == "0" * 5

    encoded_block = json.dumps(block.get_content(), sort_keys = True).encode()
    current_hash = hashlib.sha256(encoded_block).hexdigest()

    assert block.hash_value == current_hash


def test_add_reward():
    blockchain = Blockchain(False)

    fees = [13.6, 45.3, 22, 7.9, 69.42]
    expected_total = sum(fees) + blockchain.get_current_reward()
    expected_payment = Payment(PUBLIC_KEY, 0, expected_total, PUBLIC_KEY)

    for fee in fees:
        payment = Payment(PUBLIC_KEY, fee, 57, PUBLIC_KEY)
        blockchain.add_transaction(payment)

    real_total = blockchain.add_reward(wallet)
    real_payment = blockchain.transactions[0]

    assert math.isclose(real_total, expected_total)
    assert real_payment.sender == expected_payment.sender
    assert real_payment.fee == expected_payment.fee
    assert math.isclose(real_payment.amount, expected_payment.amount)
    assert real_payment.receiver == expected_payment.receiver


def test_get_balance():
    inputs = [
        [
            Block(None, [
                Payment(
                    sender="Mateus",
                    fee=0,
                    amount=100,
                    receiver="Mateus"
                )
            ], None),

            Block(None, [
                Payment(
                    sender="Miner",
                    fee=0,
                    amount=112,
                    receiver="Miner"
                ),
                Payment(
                    sender="Mateus",
                    fee=5,
                    amount=35,
                    receiver="Lucas"
                ),
                Payment(
                    sender="Lucas",
                    fee=7,
                    amount=18,
                    receiver="João"
                )
            ], None)
        ],
        [
            Block(None, [
                Payment(
                    sender="Mateus",
                    fee=0,
                    amount=100,
                    receiver="Mateus"
                )
            ], None),

            Block(None, [
                Payment(
                    sender="Marcos",
                    fee=0,
                    amount=100,
                    receiver="Marcos"
                )
            ], None),

            Block(None, [
                Payment(
                    sender="Miner",
                    fee=0,
                    amount=122,
                    receiver="Miner"
                ),
                Payment(
                    sender="Mateus",
                    fee=5,
                    amount=10,
                    receiver="Lucas"
                ),
                Payment(
                    sender="Lucas",
                    fee=2,
                    amount=3,
                    receiver="João"
                ),
                Payment(
                    sender="Marcos",
                    fee=15,
                    amount=15,
                    receiver="Lucas"
                )
            ], None)
        ]
    ]

    outputs = [
        {
            "Miner": 112,
            "Mateus": 60,
            "Lucas": 10
        },
        {
            "Miner": 122,
            "Mateus": 85,
            "Lucas": 20,
            "Marcos": 70
        }
    ]

    blockchain = Blockchain(False)

    for i in range(len(inputs)):
        blockchain.chain = inputs[i]

        for public_key in outputs[i]:
            real_output = blockchain.get_balance(public_key)
            assert real_output == outputs[i][public_key]
