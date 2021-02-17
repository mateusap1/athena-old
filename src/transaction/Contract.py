from transaction.Transaction import Transaction
from utils.transaction_utils import compare_signature

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii


class Contract(Transaction):

    def __init__(self, sender: str, fine: float, rules: list, judges: list, signatures: list):
        self.sender = sender
        self.fine = fine
        self.rules = rules
        self.judges = judges
        self.signatures = signatures

        self.signature = None
    
    def add_signature(self, private_key: str) -> str:
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(private_key)))
        h = SHA256.new(str(self.get_content()).encode('utf8'))
        signature = signer.sign(h)

        hex_signature = binascii.hexlify(signature).decode('ascii')
        self.signatures.append(hex_signature)

        return hex_signature
    
    def is_public_key_in(self, public_key: str) -> bool:
        for signature in self.signatures:
            if compare_signature(public_key, signature, str(self.get_content())):
                return True
        
        return False
    
    def is_valid(self):
        if compare_signature(self.sender, self.signature, str(self.get_content())) is False:
            return False
        
        if len(self.rules) == 0:
            return False
        
        if self.fine <= 0:
            return False
        
        return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' rules on a dictionary format"""

        return {
            "sender": self.sender,
            "signature": self.signature,
            "fine": self.fine,
            "rules": self.rules,
            "judges": self.judges,
            "signatures": self.signatures
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "fine": self.fine,
            "rules": self.rules,
            "judges": self.judges
        }
