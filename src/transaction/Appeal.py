from __future__ import annotations

from transaction.Transaction import Transaction
from transaction.Verdict import Verdict
from identity import ID
from config import verdict_config
from utils import compare_signature, sign, random_word, import_key

from Crypto.PublicKey.RSA import RsaKey
from typing import Optional

import random


class Appeal(Transaction):
    sender: ID
    verdict: Verdict
    signature: Optional[str]

    def __init__(self, sender: ID, verdict: Verdict, signature: Optional[str] = None):
        
        if not isinstance(sender, ID):
            raise TypeError("\"sender\" must be of type ID")
        elif not isinstance(verdict, Verdict):
            raise TypeError("\"verdict\" must be of type Verdict")
        elif not (signature is None or isinstance(signature, str)):
            raise TypeError("\"signature\" must be of type str")

        self.__sender = sender
        self.__verdict = verdict
        self.__signature = signature

    def is_valid(self):
        if self.__signature is None:
            print("Invalid Appeal: Unsigned transaction")
            return False

        if self.__sender.is_valid() is False:
            print("Invalid Appeal: Sender's ID is not valid")
            return False

        if self.__verdict.is_valid() is False:
            print("Invalid Appeal: Verdict is not valid")
            return False

        if compare_signature(self.__sender.to_dict()["public_key"], self.__signature,
                             self.get_content()) is False:
            print("Invalid Verdict: Signature doesn't match public key")
            return False

        return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "verdict": self.__verdict.to_dict(),
            "signature": self.__signature
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "verdict": self.__verdict.to_dict()
        }

    def sign(self, privkey: RsaKey) -> None:
        """Adds a signature to the transaction based on it's content"""

        self.__signature = sign(privkey, self.get_content())
    
    @staticmethod
    def import_dict(transaction: dict) -> Optional[Appeal]:
        """Returns an instance of Appeal object
        based on it's dictionary version"""
        
        keys = ["sender", "verdict", "signature"]
        if any([not key in keys for key in transaction.keys()]):
            print("Invalid transaction: Keys missing")
            return None

        try:
            sender = ID(**transaction["sender"])
        except TypeError:
            print("Invalid transaction: Invalid sender ID")
            return None
        
        verdict = Verdict.import_dict(transaction["verdict"])
        if verdict is None:
            print("Invalid transaction: Verdict must be valid")
            return None

        return Appeal(sender, verdict, transaction["signature"])

    @staticmethod
    def get_random(valid: bool = True) -> dict:
        """Returns a random Appeal with it's corresponding private key"""

        id_info = ID.get_random(valid=valid)
        key, userid = id_info["private_key"], id_info["id"]
        verdict = Verdict.get_random(valid=valid)["verdict"]

        appeal = Appeal(
            userid,
            verdict
        )

        appeal.sign(import_key(key))

        return {
            "private_key": key,
            "appeal": appeal
        }