from transaction.Transaction import Transaction
from transaction.Contract import Contract


class Recon(Transaction):

    def __init__(self, sender: str, fee: float, receiver: str, contract: Contract):
        super().__init__(sender, fee)

        self.hashing = None
        self.signature = None
        self.receiver = receiver
        self.contract = contract
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "hash": self.hashing,
            "sender": self.sender,
            "signature": self.signature,
            "receiver": self.receiver,
            "contract": self.contract.to_dict(),
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "contract": self.contract.to_dict(),
            "fee": self.fee
        }