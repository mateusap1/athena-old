from transaction.Transaction import Transaction

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii


class Contract(Transaction):

    def __init__(self, sender: str, fee: float, rules: list):
        super().__init__(sender, fee)

        self.hashing = None
        self.signature = None
        self.rules = rules
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' rules on a dictionary format"""

        return {
            "hash": self.hashing,
            "sender": self.sender,
            "signature": self.signature,
            "rules": self.rules,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "rules": self.rules,
            "fee": self.fee
        }
    
    # def sign_contract(self, private_key: str):
    #     """Adds to the signatures array this private_keys signature"""

    #     signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(private_key)))
    #     h = SHA256.new(("\n".join(self.rules)).encode('utf8'))
    #     signature = signer.sign(h)

    #     self.contract_signatures.add(binascii.hexlify(signature).decode('ascii'))
    
    # def verify_signature(self, public_key_str: str) -> bool:
    #     """Checks if this public_key signed the contract"""

    #     for signature in self.contract_signatures:
    #         public_key = RSA.importKey(binascii.unhexlify(public_key_str))
    #         verifier = PKCS1_v1_5.new(public_key)
    #         h = SHA256.new(("\n".join(self.rules)).encode('utf8'))

    #         if verifier.verify(h, binascii.unhexlify(signature)):
    #             return True
        
    #     return False

        