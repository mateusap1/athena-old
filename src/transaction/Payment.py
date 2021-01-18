import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "../")

from transaction.Transaction import Transaction
from wallet.Wallet import Wallet


class Payment(Transaction):

    def __init__(self, sender: str, fee: float, amount: float, receiver: str):
        super().__init__(sender, fee)

        self.signature = None
        self.amount = amount
        self.receiver = receiver
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.sender,
            "signature": self.signature,
            "amount": self.amount,
            "receiver": self.receiver,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature on a dictionary format"""

        return {
            "sender": self.sender,
            "amount": self.amount,
            "receiver": self.receiver,
            "fee": self.fee
        }
    
    # Validating the payment
    def is_valid(self, blockchain):
        """Validates the transaction"""

        # TODO: Check only the transactions made before this one

        sender_balance = blockchain.get_balance(self.sender, -1, -1)

        # Checking if signature is None
        if self.signature is None:
            return False

        # Checking if the signature matches the content
        if not Wallet.verify_transaction(self):
            return False
        
        print(self.amount, sender_balance, sender_balance < (self.fee + self.amount))
        # Checking if the sender is capable of paying the fees
        if sender_balance < (self.fee + self.amount):
            return False
        
        if self.fee < 0:
            return False
        
        if self.amount < 0:
            return False
        
        return True