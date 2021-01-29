import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain
from transaction.Transaction import Transaction
from transaction.Payment import Payment
from transaction.Contract import Contract
# from transaction.Acusation import Acusation
from wallet.Wallet import Wallet
from bit import PrivateKey, PrivateKeyTestnet, verify_sig

import pytest

# private: '3082025b0201000281810098d0f0517c865e75fae9167200bb7a39c0947174467f6a0f52f715acf4103da4d1af9e51af781413ff8738435f1e4d771d24cd605149ccde2161f3d2893c2f3fa9641be3cdf45653a5c7ea02e925f1e7fad887bcde3629df5e8e7006c6c18fb212118d0665e61cf0e0ea78cb505b726ab0f8560e500c7e968a5c2baeee6713d302030100010281803e988f68018714d864efe766c950022ff7e7965597af0765c1893e92bae2902d9c4ac0a21b2b27a64d6c392ab7a2b4fe8eac8d87dfa4484bd106cb9638eab33b512345120de9a466860ef20899e674fd418d90d9b972bb3c438ceea8ed1dc964ca05f08a721002cc80a69547c7cfda2fe67729ae16d1e934bf35b9db2ba6ca61024100b8f35a1d23221db1947fb531d4f9a1bc2d698bfdad85ff1a69cb73f917470d0c27120a895b5239732d9f42e4ca204fd47c0d2d5a302e5910cf031d7357556f03024100d38561be3f37a0604841016e28ffe9de84067db90bc752f47f08fa7da976c46c6b8a1a966bc6ae0dfd1ce73e0240ccb4b285064dd58adb5f3877db62f84a86f102401dae07b7074d51408f191365c4ccae94b920e7f334a67d32aae99859cfcf7a1b8a258e054edf5a12ceae7118b00b116482e7c67063acfc64032477d46b9e6d2b0240290a7c4899a3856ea91653dcb7ffcfb4e911095bda3936935202bff799e5fd7ebbeef3f1b3bfbd0de1cab5e386346483bb0fac8575a597a30625db5f7ca5994102402f52b4579b12874ad9df6220c13e2bdfc3b43ae637efbdae8f6056727055d0bb13863ee882228f472599cb46bdf8bd506ef5fe19ec7dd6fb43866cb3afd91d5d', 
# public: '30819f300d06092a864886f70d010101050003818d003081890281810098d0f0517c865e75fae9167200bb7a39c0947174467f6a0f52f715acf4103da4d1af9e51af781413ff8738435f1e4d771d24cd605149ccde2161f3d2893c2f3fa9641be3cdf45653a5c7ea02e925f1e7fad887bcde3629df5e8e7006c6c18fb212118d0665e61cf0e0ea78cb505b726ab0f8560e500c7e968a5c2baeee6713d30203010001'

# Initializing wallet so we can have a testing public and private key
wallet = Wallet()

def test_payment():
    blockchain = Blockchain(False)

    payment = Payment(wallet.public_key, 13, 57, wallet.public_key)
    wallet.sign_transaction(payment)

    assert wallet.verify_transaction(payment) == True
    assert payment.to_dict() == {
        "sender": wallet.public_key,
        "signature": payment.signature,
        "amount": 57,
        "receiver": wallet.public_key,
        "fee": 13
    }
    assert payment.get_content() == {
        "sender": wallet.public_key,
        "amount": 57,
        "receiver": wallet.public_key,
        "fee": 13
    }

# TODO: Finish this test
def test_contract():
    """Testing if contract transactions are working"""

    blockchain = Blockchain(False)

    public_key = "30819f300d06092a864886f70d010101050003818d003081890281810098d0f0517c865e75fae9167200bb7a39c0947174467f6a0f52f715acf4103da4d1af9e51af781413ff8738435f1e4d771d24cd605149ccde2161f3d2893c2f3fa9641be3cdf45653a5c7ea02e925f1e7fad887bcde3629df5e8e7006c6c18fb212118d0665e61cf0e0ea78cb505b726ab0f8560e500c7e968a5c2baeee6713d30203010001"
    private_key = "3082025b0201000281810098d0f0517c865e75fae9167200bb7a39c0947174467f6a0f52f715acf4103da4d1af9e51af781413ff8738435f1e4d771d24cd605149ccde2161f3d2893c2f3fa9641be3cdf45653a5c7ea02e925f1e7fad887bcde3629df5e8e7006c6c18fb212118d0665e61cf0e0ea78cb505b726ab0f8560e500c7e968a5c2baeee6713d302030100010281803e988f68018714d864efe766c950022ff7e7965597af0765c1893e92bae2902d9c4ac0a21b2b27a64d6c392ab7a2b4fe8eac8d87dfa4484bd106cb9638eab33b512345120de9a466860ef20899e674fd418d90d9b972bb3c438ceea8ed1dc964ca05f08a721002cc80a69547c7cfda2fe67729ae16d1e934bf35b9db2ba6ca61024100b8f35a1d23221db1947fb531d4f9a1bc2d698bfdad85ff1a69cb73f917470d0c27120a895b5239732d9f42e4ca204fd47c0d2d5a302e5910cf031d7357556f03024100d38561be3f37a0604841016e28ffe9de84067db90bc752f47f08fa7da976c46c6b8a1a966bc6ae0dfd1ce73e0240ccb4b285064dd58adb5f3877db62f84a86f102401dae07b7074d51408f191365c4ccae94b920e7f334a67d32aae99859cfcf7a1b8a258e054edf5a12ceae7118b00b116482e7c67063acfc64032477d46b9e6d2b0240290a7c4899a3856ea91653dcb7ffcfb4e911095bda3936935202bff799e5fd7ebbeef3f1b3bfbd0de1cab5e386346483bb0fac8575a597a30625db5f7ca5994102402f52b4579b12874ad9df6220c13e2bdfc3b43ae637efbdae8f6056727055d0bb13863ee882228f472599cb46bdf8bd506ef5fe19ec7dd6fb43866cb3afd91d5d"
    
    transaction_signature = "3d8e25a7c73552fe62107bedd73054a79af6c4de26677c88ca2287e3fe5a897603b43c59fed7d04309385e4b8d124d450e07505fb2e653506f62034253dbabb04795c741231e18f8e53768827ee78b1f10ddaa54045d6dcca40ecd0ea18cf99c481abe6abcb870f817e106a425fd69660d0fed33fda287439f89f11f72a7b951"
    contract_signature = "91128b8bded9ee089d899cdafcfbbe494e38083cbe20ee8611ac55532724f4581964b9c31065db0e54347876516ae20c2f604c5d52676330f5bcce543a3fc22eaae756dafc509e390aaec02f511db515a775f522a170735f87100beed44690e2767cf1121c12e7f93fa7677a0f62dbd2b8830abcb2bfd3df8d1601af99f12e5c"

    contract = Contract(public_key, 7, ["NAP"])
    contract.signature = transaction_signature

    contract.contract_signatures.add(contract_signature)

    assert wallet.verify_transaction(contract) == True
    assert contract.to_dict() == {
        "sender": public_key,
        "signature": "3d8e25a7c73552fe62107bedd73054a79af6c4de26677c88ca2287e3fe5a897603b43c59fed7d04309385e4b8d124d450e07505fb2e653506f62034253dbabb04795c741231e18f8e53768827ee78b1f10ddaa54045d6dcca40ecd0ea18cf99c481abe6abcb870f817e106a425fd69660d0fed33fda287439f89f11f72a7b951",
        "rules": ["NAP"],
        "contract_signatures": set([contract_signature]),
        "fee": 7
    }
    assert contract.get_content() == {
        "sender": public_key,
        "rules": ["NAP"],
        "contract_signatures": set([contract_signature]),
        "fee": 13
    }
    assert contract.verify_signature(public_key) == True



# def test_max_transactions():
#     """Tesing if 'Transaction' method 'max_transaction()' is working properly"""

#     blockchain = Blockchain(False)

#     expected_output = []

#     sender = wallet.public_key
#     fee = 3
#     amount = 1
#     receiver = "<receiver>"

#     transaction = Payment(sender, fee, amount, receiver)
#     signature = wallet.sign_transaction(transaction)

#     # Adding a "malicious" transaction to the list
#     blockchain.transactions.append(transaction)

#     sender = wallet.public_key
#     fee = 0
#     amount = 0
#     receiver = "<receiver>"

#     transaction = Payment(sender, fee, amount, receiver)
#     signature = wallet.sign_transaction(transaction)

#     # Adding a real transaction to the list
#     blockchain.add_transaction(transaction)
#     expected_output.append(transaction)

#     sender = wallet.public_key
#     fee = 0
#     amount = 0
#     receiver = "<receiver>"

#     transaction = Payment(sender, fee, amount, receiver)
#     transaction.signature = signature # False signature

#     # Adding another "malicious" transaction to the list
#     blockchain.transactions.append(transaction)

#     sender = wallet.public_key
#     fee = 0
#     content = ["You shall not kill"]

#     transaction = Contract(sender, fee, content)
#     signature = wallet.sign_transaction(transaction)

#     # Adding another real transaction to the list
#     blockchain.add_transaction(transaction)
#     expected_output.append(transaction)

#     expected_output.sort(key = lambda x : x.fee, reverse = True)

#     assert Transaction.max_transactions(blockchain) == expected_output
