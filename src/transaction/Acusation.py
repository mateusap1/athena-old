import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "../")

from transaction.Contract import Contract
from transaction.Transaction import Transaction
from Blockchain import Blockchain
from wallet.Wallet import Wallet


class Judgement(Transaction):

    def __init__(self, sender: str, fee: float, contract: Contract, accuser: str,
                 defendant: str, violation_index: int, violation_proof: str):
        super().__init__(sender, fee)

        self.signature = None
        # The contract that is being broken
        self.contract = contract
        # The accuser public_key
        self.accuser = accuser
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
            "accuser": self.accuser,
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
            "accuser": self.accuser,
            "defendant": self.defendant,
            "violation_index": self.violation_index,
            "violation_proof": self.violation_proof,
            "fee": self.fee
        }