from __future__ import annotations

from transaction.Transaction import Transaction
from utils import compare_signature, parse_key, import_key, sign
from identity import ID
from config import contract_config

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii
import datetime


MIN_JUDGES = contract_config["minimum_judges"]
MAX_JUDGES = contract_config["maximum_judges"]
MIN_RULES = contract_config["minimum_rules"]
MAX_RULES = contract_config["maximum_rules"]
SENDER_CAN_JUDGE = contract_config["allow_sender_to_judge"]


class Contract(Transaction):

    def __init__(self, privkey: RsaKey, sender: ID, rules: list,
                 judges: list, expire: datetime.datetime):
        self.__private_key = privkey
        self.__sender = sender
        self.__rules = rules
        self.__judges = judges
        self.__expire = expire

        self.sign()

    # TODO: Remove this method, as signatures will be independent from contracts
    def add_signature(self, private_key: str) -> str:
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(private_key)))
        h = SHA256.new(str(self.get_content()).encode('utf8'))
        signature = signer.sign(h)

        hex_signature = binascii.hexlify(signature).decode('ascii')
        self.signatures.append(hex_signature)

        return hex_signature

    # TODO: Remove this method, as signatures will be independent from contracts
    def is_public_key_in(self, public_key: str) -> bool:
        for signature in self.signatures:
            if compare_signature(public_key, signature, str(self.get_content())):
                return True

        return False

    def is_valid(self):
        if self.__sender.is_valid() is False:
            return False

        seen = set()
        for judge in self.__judges:
            if isinstance(judge, ID) is False:
                # Check if judge is an ID

                print("Invalid Contract: Judge must be of type \"ID\"")
                return False
            elif judge.is_valid() is False:
                # Check if the ID is valid

                print("Invalid Contract: Judge must be a valid ID")
                return False
            elif not SENDER_CAN_JUDGE and judge.to_dict() == self.__sender.to_dict():
                # Check if the sender is a judge

                print("Invalid Contract: Sender can't be a judge")
                return False
            elif judge in seen:
                # Check if judge is repeated

                print("Invalid Contract: Judge repeated \"ID\"")
                return False

            seen.add(judge)

        if self.__expire < datetime.datetime.now():
            # Verify if the contract already expired

            print("Invalid Contract: Contract expired")
            return False

        if not (MIN_RULES <= len(self.__rules) <= MAX_RULES):
            print(f"Invalid Contract: You must have a maximum of {MAX_RULES} " +
                  f"and a minimum of {MIN_RULES} rules")
            return False

        if not (MIN_JUDGES <= len(self.__judges) <= MAX_JUDGES):
            print(f"Invalid Contract: You must have a maximum of {MAX_JUDGES} " +
                  f"and a minimum of {MIN_JUDGES} judges")
            return False

        if compare_signature(self.__sender.to_dict()["public_key"], self.__signature,
                             self.get_content()) is False:
            print("Invalid Contract: Signature doesn't match public key")
            return False

        return True

    def to_dict(self) -> dict:
        """Returns all class paramaters in a dictionary form"""

        return {
            "sender": self.__sender.to_dict(),
            "signature": self.__signature,
            "rules": self.__rules,
            "judges": [i.to_dict() for i in self.__judges],
            "expire": str(self.__expire)
        }

    def get_content(self) -> dict:
        """Returns only the class paramaters that can be hashed"""

        return {
            "sender": self.__sender.to_dict(),
            "rules": self.__rules,
            "judges": [i.to_dict() for i in self.__judges],
            "expire": str(self.__expire)
        }

    def sign(self) -> None:
        """Adds a signature to the transaction based on it's content"""

        self.__signature = sign(self.__private_key, self.get_content())

    @staticmethod
    def get_random() -> dict:
        """Returns a random valid Contract with it's corresponding private key"""

        N = 1

        id_info = ID.get_random()
        key, userid = id_info["private_key"], id_info["id"]

        contract = Contract(
            import_key(key),
            userid,
            ["You shall not kill", "You shall not steal"],
            [ID.get_random()["id"] for _ in range(N)],
            datetime.datetime.now() + datetime.timedelta(days=7)
        )

        return {
            "private_key": key,
            "contract": contract
        }
