from transaction.Transaction import Transaction
from transaction.Accusation import Accusation


class Veredict(Transaction):

    def __init__(self, sender: str, fee: float, accusation: Accusation, is_guilty: bool, description: str):
        super().__init__(sender, fee)

        self.hashing = None
        self.signature = None
        self.accusation = accusation
        self.is_guilty = is_guilty
        self.description = description
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "hash": self.hashing,
            "sender": self.sender,
            "signature": self.signature,
            "accusation": self.accusation.to_dict(),
            "is_guilty": self.is_guilty,
            "description": self.description,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "accusation": self.accusation.to_dict(),
            "is_guilty": self.is_guilty,
            "description": self.description,
            "fee": self.fee
        }