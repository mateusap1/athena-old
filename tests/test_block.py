import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Block import Block
from Blockchain import Blockchain
from transaction.Payment import Payment
from wallet.Wallet import Wallet


def test_block_validation():
    blockchain = Blockchain(False)
    wallet = Wallet()

    transaction = Payment(wallet.public_key, 0, 100, wallet.public_key)
    wallet.sign_transaction(transaction)
    blockchain.add_transaction(transaction)

    last_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(last_block.proof)

    block = blockchain.create_block(proof, last_block.get_hash())

    assert block.is_valid(blockchain) == True
    assert blockchain.get_balance(wallet.public_key) == 100

    wallet2 = Wallet()
    wallet3 = Wallet()

    # Now that I mined a block and I have some money I will test if the transactions are working
    transaction = Payment(wallet2.public_key, 0, 100.1, wallet2.public_key)
    wallet2.sign_transaction(transaction)
    blockchain.add_transaction(transaction)

    # Giving wallet3 50 coins while giving 0.1 of fees to wallet2
    transaction2 = Payment(wallet.public_key, 0.1, 50, wallet3.public_key)
    wallet.sign_transaction(transaction2)
    blockchain.add_transaction(transaction2)

    last_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(last_block.proof)

    block = blockchain.create_block(proof, last_block.get_hash())

    assert block.is_valid(blockchain) == True
    assert blockchain.get_balance(wallet.public_key) == 100 - 50.1
    assert blockchain.get_balance(wallet2.public_key) == 100.1
    assert blockchain.get_balance(wallet3.public_key) == 50
