from transaction.Transaction import Transaction
from transaction.Contract import Contract


class Accusation(Transaction):

    def __init__(self, sender: str, fee: float, accused: str, contract: Contract, rule_index: int, proposed_fine, judge: str):
        super().__init__(sender, fee)

        self.hashing = None
        self.signature = None
        self.accused = accused
        self.contract = contract
        self.rule_index = rule_index
        self.proposed_fine = proposed_fine
        self.judge = judge
    
    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "hash": self.hashing,
            "sender": self.sender,
            "signature": self.signature,
            "accused": self.accused,
            "contract": self.contract.to_dict(),
            "rule_index": self.rule_index,
            "proposed_fine": self.proposed_fine,
            "judge": self.judge,
            "fee": self.fee
        }
    
    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.sender,
            "accused": self.accused,
            "contract": self.contract.to_dict(),
            "rule_index": self.rule_index,
            "proposed_fine": self.proposed_fine,
            "judge": self.judge,
            "fee": self.fee
        }