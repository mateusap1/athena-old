import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from Block import Block

import pytest
import hashlib


# Checking if the transaction insertion is failing when the paramaters are wrong
def test_transaction_fail():
    blockchain = Blockchain()

    transaction_type = "Fail"
    data = {"Test": 2}

    with pytest.raises(Exception) as e:
        blockchain.add_transaction(transaction_type, data)

    assert str(e.value) == "Transaction type must be either \"fees\", \"contract\" or \"trial\""

# Checking if the transactions being inserted into the list
def test_transaction_succeed():
    blockchain = Blockchain()

    transaction_types = ["contract", "fees", "trial"]
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

    transactions = []

    for transaction_type in transaction_types:
        blockchain.add_transaction(transaction_type, data)
        transactions.append({
            "transaction_type": transaction_type,
            "data": data
        })

    assert blockchain.transactions == transactions

# Checking if the proof of work of the blocks that are being created are correct
def test_create_block():
    blockchain = Blockchain()
    block = blockchain.get_previous_block()
    proof = block.proof
    previous_hash = block.get_hash()
    new_proof = blockchain.proof_of_work(proof)

    new_block = blockchain.create_block(new_proof, previous_hash)
    hash_operation = hashlib.sha256(str(new_block.proof**2 - proof**2).encode()).hexdigest()

    difficulty = blockchain.difficulty

    assert hash_operation[:difficulty] == "0" * difficulty

def test_chain_validation():
    blockchain = Blockchain()

    chain = [Block(1, 1, 1, 1, 1), Block(1, 1, 1, 1, 1)]

    assert blockchain.is_chain_valid(chain) == False

def test_difficulty_adapter1():
    blockchain = Blockchain()

    new_proof = 0
    while True:
        hash_operation = hashlib.sha256(str(new_proof**2 - 1**2).encode()).hexdigest()
        if hash_operation[:4] == "0000":
            break
        new_proof += 1

    chain = [Block(1, "2018-12-04 09:41:09.0", [], 1, 1), Block(1, "2018-12-04 09:41:16.0", [], new_proof, "00000a")]
    blockchain.chain = chain
    assert blockchain.get_mining_difficulty() == 5

def test_difficulty_adapter2():
    blockchain = Blockchain()

    new_proof = 0
    while True:
        hash_operation = hashlib.sha256(str(new_proof**2 - 1**2).encode()).hexdigest()
        if hash_operation[:4] == "0000":
            break
        new_proof += 1

    chain = [Block(1, "2018-12-04 09:41:09.0", [], 1, 1), Block(1, "2018-12-04 09:41:17.0", [], new_proof, "00000a")]
    blockchain.chain = chain
    assert blockchain.get_mining_difficulty() == 4