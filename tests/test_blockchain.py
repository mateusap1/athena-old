import sys
import os
import hashlib
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from Block import Block
from wallet.Wallet import Wallet
from transaction.Payment import Payment


wallet = Wallet()

def test_create_block():
    blockchain = Blockchain(False)
    block = blockchain.get_previous_block()
    proof = block.proof
    previous_hash = block.hashing
    new_proof = blockchain.proof_of_work(proof)

    new_block = blockchain.create_block(new_proof, previous_hash)

    expected_result = Block(2, new_block.timestamp, [], 533, previous_hash)
    expected_result.hash()

    assert new_block.hashing == expected_result.hashing
    assert new_block.index == expected_result.index
    assert new_block.transactions == expected_result.transactions
    assert new_block.proof == expected_result.proof
    assert new_block.get_dict() == expected_result.get_dict()

def test_get_mining_difficulty():
    blockchain = Blockchain(False)

    chains = [
        [
            Block(None, "2018-12-04 09:41:09.0", None, 1, None),
            Block(None, "2018-12-04 09:41:17.0", None, 533, None)
        ],
        [
            Block(None, "2018-12-04 09:41:09.0", None, 1, None),
            Block(None, "2018-12-04 09:41:16.0", None, 533, None)
        ],
        [
            Block(None, "2018-12-04 09:41:09.0", None, 1, None),
            Block(None, "2018-12-04 09:41:16.0", None, 533, None),
            Block(None, "2018-12-04 09:41:23.0", None, 912758, None)
        ]
    ]

    expected_outputs = [4, 5, 6]

    for i, chain in enumerate(chains):
        blockchain.chain = chain
        blockchain.get_mining_difficulty()
        assert blockchain.get_mining_difficulty() == expected_outputs[i]

def test_proof_of_work():
    blockchain = Blockchain(False)

    inputs = [(4, 1), (5, 1), (6, 245)]
    expected_outputs = [533, 632238, 2220697]

    for i in range(len(inputs)):
        blockchain.difficulty = inputs[i][0]
        real_output = blockchain.proof_of_work(inputs[i][1])

        assert real_output == expected_outputs[i]

def test_get_balance():
    inputs = [
        [
            Block(None, None, [
                Payment(
                    sender = "Mateus",
                    fee = 0,
                    amount = 100,
                    receiver = "Mateus"
                )
            ], None, None),

            Block(None, None, [
                Payment(
                    sender = "Miner",
                    fee = 0,
                    amount = 112,
                    receiver = "Miner"
                ),
                Payment(
                    sender = "Mateus",
                    fee = 5,
                    amount = 35,
                    receiver = "Lucas"
                ),
                Payment(
                    sender = "Lucas",
                    fee = 7,
                    amount = 18,
                    receiver = "João"
                )
            ], None, None)
        ],
        [
            Block(None, None, [
                Payment(
                    sender = "Mateus",
                    fee = 0,
                    amount = 100,
                    receiver = "Mateus"
                )
            ], None, None),

            Block(None, None, [
                Payment(
                    sender = "Marcos",
                    fee = 0,
                    amount = 100,
                    receiver = "Marcos"
                )
            ], None, None),

            Block(None, None, [
                Payment(
                    sender = "Miner",
                    fee = 0,
                    amount = 122,
                    receiver = "Miner"
                ),
                Payment(
                    sender = "Mateus",
                    fee = 5,
                    amount = 10,
                    receiver = "Lucas"
                ),
                Payment(
                    sender = "Lucas",
                    fee = 2,
                    amount = 3,
                    receiver = "João"
                ),
                Payment(
                    sender = "Marcos",
                    fee = 15,
                    amount = 15,
                    receiver = "Lucas"
                )
            ], None, None)
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