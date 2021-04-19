from transaction.Transaction import Transaction
from transaction.Verdict import Verdict
from identity import ID
from config import verdict_config
from utils import compare_signature, sign, random_word, import_key
from Crypto.PublicKey.RSA import RsaKey

import random


class Appeal(Transaction):

    def __init__(self, privkey: RsaKey, sender: ID, verdict: Verdict):

        if not isinstance(privkey, RsaKey):
            raise TypeError("\"privkey\" must be of type RsaKey")
        elif not isinstance(sender, ID):
            raise TypeError("\"sender\" must be of type ID")
        elif not isinstance(verdict, Verdict):
            raise TypeError("\"verdict\" must be of type Verdict")

        self.__private_key = privkey
        self.__sender = sender
        self.__verdict = verdict

        self.sign()

    def is_valid(self):
        if self.__sender.is_valid() is False:
            print("Invalid Appeal: Sender's ID is not valid")
            return False
        elif self.__verdict.is_valid() is False:
            print("Invalid Appeal: Verdict is not valid")
            return False
        elif compare_signature(self.__sender.to_dict()["public_key"], self.__signature,
                               self.get_content()) is False:
            print("Invalid Verdict: Signature doesn't match public key")
            return False
        else:
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

    def sign(self) -> None:
        """Adds a signature to the transaction based on it's content"""

        self.__signature = sign(self.__private_key, self.get_content())

    @staticmethod
    def get_random(valid: bool = True) -> dict:
        """Returns a random Appeal with it's corresponding private key"""

        id_info = ID.get_random(valid=valid)
        key, userid = id_info["private_key"], id_info["id"]
        verdict = Verdict.get_random(valid=valid)["verdict"]

        appeal = Appeal(
            import_key(key),
            userid,
            verdict
        )

        return {
            "private_key": key,
            "appeal": appeal
        }
