from __future__ import annotations

from transaction.Transaction import Transaction
from transaction.Contract import Contract
from utils import compare_signature, import_key, sign
from identity import ID

from Crypto.PublicKey.RSA import RsaKey
from typing import Optional


class Accusation(Transaction):
    sender: ID
    accused: ID
    contract: Contract
    signature: Optional[str]

    def __init__(self, sender: ID, accused: ID, contract: Contract, 
                 signature: Optional[str] = None):
                 
        if not isinstance(sender, ID):
            raise TypeError("\"sender\" must be of type ID")
        elif not isinstance(accused, ID):
            raise TypeError("\"accused\" must be of type ID")
        elif not isinstance(contract, Contract):
            raise TypeError("\"contract\" must be of type Contract")
        elif not (signature is None or isinstance(signature, str)):
            raise TypeError("\"signature\" must be of type str")

        self.__sender = sender
        self.__accused = accused
        self.__contract = contract
        self.__signature = signature

    def is_valid(self):
        if self.__signature is None:
            print("Invalid Appeal: Unsigned transaction")
            return False

        if self.__sender.is_valid() is False:
            print("Invalid Accusation: Sender's ID is not valid")
            return False

        if self.__accused.is_valid() is False:
            print("Invalid Accusation: Accused's ID is not valid")
            return False

        if self.__contract.is_valid() is False:
            print("Invalid Accusation: You must provide a valid contract")
            return False

        if compare_signature(self.__sender.to_dict()["public_key"], self.__signature,
                             self.get_content()) is False:
            print("Invalid Accusation: Signature doesn't match public key")
            return False

        return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "accused": self.__accused.to_dict(),
            "contract": self.__contract.to_dict(),
            "signature": self.__signature
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "accused": self.__accused.to_dict(),
            "contract": self.__contract.to_dict()
        }

    def sign(self, privkey: RsaKey) -> None:
        """Adds a signature to the transaction based on it's content"""

        self.__signature = sign(privkey, self.get_content())
    
    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
    
    @staticmethod
    def import_dict(transaction: dict) -> Optional[Accusation]:
        keys = ["sender", "accused", "contract", "signature"]
        if any([not key in keys for key in transaction.keys()]):
            print("Invalid transaction: Keys missing")
            return None

        try:
            sender = ID(**transaction["sender"])
        except TypeError:
            print("Invalid transaction: Invalid sender ID")
            return None
        
        try:
            accused = ID(**transaction["accused"])
        except TypeError:
            print("Invalid transaction: Invalid accused ID")
            return None

        contract = Contract.import_dict(transaction["contract"])
        if contract is None:
            print("Invalid transaction: Contract must be valid")
            return None

        return Accusation(sender, accused, contract, transaction["signature"])

    @staticmethod
    def get_random(valid: bool = True) -> dict:
        """Returns a random Accusation with it's corresponding private key"""

        id_info = ID.get_random(valid=valid)
        key, userid = id_info["private_key"], id_info["id"]

        accusation = Accusation(
            userid,
            ID.get_random()["id"],
            Contract.get_random()["contract"]
        )

        accusation.sign(import_key(key))

        return {
            "private_key": key,
            "accusation": accusation
        }