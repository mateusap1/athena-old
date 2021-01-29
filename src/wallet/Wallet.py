from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii

# Most part of this code was written by @adi2381 and you can find it here: https://github.com/adi2381/py-blockchain

class Wallet:

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.create_keys()
    
    @staticmethod
    def generate_keys():
        """Generating a new pair of private and public key"""

        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()

        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def create_keys(self):
        """Create a new pair of private and public keys"""
        private_key, public_key = Wallet.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def sign_transaction(self, transaction):
        """Sign a transaction and return the signature"""
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key))) # RSA is a cryptography algorithm
        h = SHA256.new(str(transaction.get_content()).encode('utf8'))
        signature = signer.sign(h)

        # binascii.hexlify is used to convert binary data to hexadecimal representation
        transaction.sign(binascii.hexlify(signature).decode('ascii'))

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(str(transaction.get_content()).encode('utf8'))

        return verifier.verify(h, binascii.unhexlify(transaction.signature))
    
    def get_balance(self, blockchain):
        balance = 0
        for block in blockchain.chain:
            for transaction in block.transactions:
                if isinstance(transaction, Payment):
                    if transaction.receiver == self.public_key:
                        balance += transaction.amount
                    elif transaction.sender == self.public_key:
                        balance -= transaction.amount
                        balance -= transaction.fee
        
        return balance