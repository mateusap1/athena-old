from transaction.Transaction import Transaction
from transaction.Contract import Contract
from utils.transaction_utils import compare_signature


class Accusation(Transaction):

    def __init__(self, sender: str, accused: str, contract: Contract):
        self.sender = sender
        self.accused = accused
        self.contract = contract
        
        self.signature = None
    
    def is_valid(self):
        if compare_signature(self.sender, self.signature, str(self.get_content())) is False:
            return False
        
        if self.contract.is_public_key_in(self.accused) is False:
            return False
        
        return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.sender,
            "signature": self.signature,
            "accused": self.accused,
            "contract": self.contract.to_dict()
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "accused": self.accused,
            "contract": self.contract.to_dict()
        }
