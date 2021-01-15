import sys
import os
import hashlib

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from Block import Block
from Wallet.Wallet import Wallet


wallet = Wallet()

# Checking if the proof of work of the blocks that are being created are correct
def test_create_block():
    blockchain = Blockchain(False)
    block = blockchain.get_previous_block()
    proof = block.proof
    previous_hash = block.get_hash()
    new_proof = blockchain.proof_of_work(proof)

    new_block = blockchain.create_block(new_proof, previous_hash)
    hash_operation = hashlib.sha256(str(new_block.proof**2 - proof**2).encode()).hexdigest()

    difficulty = blockchain.difficulty

    assert hash_operation[:difficulty] == "0" * difficulty

def test_chain_validation():
    blockchain = Blockchain(False)

    chain = [Block(1, 1, 1, 1, 1), Block(1, 1, 1, 1, 1)]

    assert blockchain.is_chain_valid(chain) == False

def test_difficulty_adapter1():
    blockchain = Blockchain(False)

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
    blockchain = Blockchain(False)

    new_proof = 0
    while True:
        hash_operation = hashlib.sha256(str(new_proof**2 - 1**2).encode()).hexdigest()
        if hash_operation[:4] == "0000":
            break
        new_proof += 1

    chain = [Block(1, "2018-12-04 09:41:09.0", [], 1, 1), Block(1, "2018-12-04 09:41:17.0", [], new_proof, "00000a")]
    blockchain.chain = chain
    assert blockchain.get_mining_difficulty() == 4

def test_block_validation():
    blockchain = Blockchain(False)

    sender = wallet.public_key

    transaction = [
        sender,
        "contract", 
        {"test": 0}, 
        {
            "value": 8,
            "receipt": "<receipt>"
        }
    ]

    signature = wallet.sign_transaction(*transaction)
    transaction.append(signature)

    for i in range(1000):
        blockchain.add_transaction(*transaction)
    
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block.proof
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block.get_hash()

    block = blockchain.create_block(proof, previous_hash)

    assert block.is_valid() == False