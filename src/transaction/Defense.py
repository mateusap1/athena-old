from transaction.Transaction import Transaction
from transaction.Accusation import Accusation


class Defense(Transaction):

    def __init__(self, sender: str, fee: float, accusation: Accusation, judge: str):
        super().__init__(sender, fee)

        self.hashing = None
        self.signature = None
        self.accusation = accusation
        self.judge = judge
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "hash": self.hashing,
            "sender": self.sender,
            "signature": self.signature,
            "accusation": self.accusation.to_dict(),
            "judge": self.judge,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "accusation": self.accusation.to_dict(),
            "judge": self.judge,
            "fee": self.fee
        }