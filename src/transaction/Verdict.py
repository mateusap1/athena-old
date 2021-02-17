from transaction.Transaction import Transaction
from transaction.Accusation import Accusation


class Verdict(Transaction):

    def __init__(self, sender: str, accusation: Accusation, is_guilty: bool, description: str):
        self.sender = sender
        self.accusation = accusation
        self.is_guilty = is_guilty
        self.description = description

        self.signature = None
    
    def is_valid(self):
        if compare_signature(self.sender, self.signature, str(self.get_content())) is False:
            return False
        
        contract = self.accusation.contract
        judges = contract.judges
        
        if self.sender in judges is False:
            return False
        
        return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.sender,
            "signature": self.signature,
            "accusation": self.accusation.to_dict(),
            "is_guilty": self.is_guilty,
            "description": self.description
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "accusation": self.accusation.to_dict(),
            "is_guilty": self.is_guilty,
            "description": self.description
        }
