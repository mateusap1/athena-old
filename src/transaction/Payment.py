from transaction.Transaction import Transaction


class Payment(Transaction):

    def __init__(self, sender: str, fee: float, amount: float, receiver: str):
        super().__init__(sender, fee)

        self.hashing = None
        self.signature = None
        self.amount = amount
        self.receiver = receiver
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "hash": self.hashing,
            "sender": self.sender,
            "signature": self.signature,
            "amount": self.amount,
            "receiver": self.receiver,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "amount": self.amount,
            "receiver": self.receiver,
            "fee": self.fee
        }