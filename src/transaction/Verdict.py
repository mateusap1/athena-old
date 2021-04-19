from transaction.Transaction import Transaction
from transaction.Accusation import Accusation
from identity import ID
from config import verdict_config
from utils import compare_signature, sign, random_word, import_key
from Crypto.PublicKey.RSA import RsaKey

import random


SENTECE_CHAR_LIMIT = verdict_config["sentence_char_limit"]
DESCRIPTION_CHAR_LIMIT = verdict_config["description_char_limit"]


class Verdict(Transaction):

    def __init__(self, privkey: RsaKey, sender: ID, accusation: Accusation,
                 sentence: str, description: str):

        if not isinstance(privkey, RsaKey):
            raise TypeError("\"privkey\" must be of type RsaKey")
        elif not isinstance(sender, ID):
            raise TypeError("\"sender\" must be of type ID")
        elif not isinstance(accusation, Accusation):
            raise TypeError("\"accusation\" must be of type Accusation")
        elif not isinstance(sentence, str):
            raise TypeError("\"sentence\" must be of type str")
        elif not isinstance(description, str):
            raise TypeError("\"description\" must be of type str")

        self.__private_key = privkey
        self.__sender = sender
        self.__accusation = accusation
        self.__sentence = sentence
        self.__description = description

        self.sign()

    def is_valid(self):
        if self.__sender.is_valid() is False:
            print("Invalid Verdict: Sender's ID is not valid")
            return False
        elif self.__accusation.is_valid() is False:
            print("Invalid Verdict: Accusation is not valid")
            return False
        elif compare_signature(self.__sender.to_dict()["public_key"], self.__signature,
                               self.get_content()) is False:
            print("Invalid Verdict: Signature doesn't match public key")
            return False
        elif len(self.__sentence) == 0:
            print("Invalid Verdict: The sentence must have at least one character")
            return False
        elif len(self.__sentence) > SENTECE_CHAR_LIMIT:
            print("Invalid Verdict: The sentence surpassed the " +
                  f"characters limit of {SENTECE_CHAR_LIMIT}")
            return False
        elif len(self.__description) > DESCRIPTION_CHAR_LIMIT:
            print("Invalid Verdict: The description surpassed the " +
                  f"characters limit of {DESCRIPTION_CHAR_LIMIT}")
            return False
        else:
            return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "signature": self.__signature,
            "accusation": self.__accusation.to_dict(),
            "sentence": self.__sentence,
            "description": self.__description
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "accusation": self.__accusation.to_dict(),
            "sentence": self.__sentence,
            "description": self.__description
        }

    def sign(self) -> None:
        """Adds a signature to the transaction based on it's content"""

        self.__signature = sign(self.__private_key, self.get_content())

    @staticmethod
    def get_random(valid: bool = True) -> dict:
        """Returns a random Verdict with it's corresponding private key"""

        id_info = ID.get_random(valid=valid)
        key, userid = id_info["private_key"], id_info["id"]
        accusation = Accusation.get_random(valid=valid)["accusation"]

        verdict = Verdict(
            import_key(key),
            userid,
            accusation,
            random_word(random.randint(1, SENTECE_CHAR_LIMIT)),
            random_word(random.randint(1, DESCRIPTION_CHAR_LIMIT))
        )

        return {
            "private_key": key,
            "verdict": verdict
        }
