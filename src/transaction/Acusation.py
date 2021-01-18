import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "../")

from transaction.Contract import Contract
from transaction.Transaction import Transaction
from Blockchain import Blockchain
from wallet.Wallet import Wallet


class Acusation(Transaction):

    def __init__(self, sender: str, fee: float, contract: Contract, defendant: str, 
                 violation_index: int, violation_proof: str):
        super().__init__(sender, fee)

        self.signature = None
        # The contract that is being broken
        self.contract = contract
        # The defendant public_key
        self.defendant = defendant
        # The index of the violation on the contract
        self.violation_index = violation_index
        # The proof that the defendant commited the violation
        self.violation_proof = violation_proof
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.sender,
            "signature": self.signature,
            "contract": self.contract.to_dict(),
            "defendant": self.defendant,
            "violation_index": self.violation_index,
            "violation_proof": self.violation_proof,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature on a dictionary format"""

        return {
            "sender": self.sender,
            "contract": self.contract.to_dict(),
            "defendant": self.defendant,
            "violation_index": self.violation_index,
            "violation_proof": self.violation_proof,
            "fee": self.fee
        }
    
    def is_valid(self, blockchain: Blockchain) -> bool:
        """Validates the transaction"""

        # Checking if signature is None
        if self.signature is None:
            return False

        # Checking if the signature matches the content
        if not Wallet.verify_transaction(self):
            return False

        # Checking if the sender is capable of paying the fees
        if blockchain.get_balance(self.sender) < self.fee:
            return False
        
        if self.fee < 0:
            return False
        
        # If the defendant didn't sign the contract he can't be accused of breaking it
        if not self.contract.verify_signature(self.defendant):
            return False
        
        # If the accuser didn't sign the contract, he can't accuse anyone of breaking it either
        if not self.contract.verify_signature(self.sender):
            return False

        return True