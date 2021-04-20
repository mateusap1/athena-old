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
            "signature": self.__signature,
            "verdict": self.__verdict.to_dict()
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