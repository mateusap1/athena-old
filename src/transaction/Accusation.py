from transaction.Transaction import Transaction
from transaction.Contract import Contract
from utils import compare_signature, import_key, sign
from identity import ID

from Crypto.PublicKey.RSA import RsaKey


class Accusation(Transaction):

    def __init__(self, privkey: RsaKey, sender: ID, accused: ID, contract: Contract):

        if not isinstance(privkey, RsaKey):
            raise TypeError("\"privkey\" must be of type RsaKey")
        elif not isinstance(sender, ID):
            raise TypeError("\"sender\" must be of type ID")
        elif not isinstance(accused, ID):
            raise TypeError("\"accused\" must be of type ID")
        elif not isinstance(contract, Contract):
            raise TypeError("\"contract\" must be of type Contract")

        self.__private_key = privkey
        self.__sender = sender
        self.__accused = accused
        self.__contract = contract

        self.sign()

    def is_valid(self):
        if self.__sender.is_valid() is False:
            print("Invalid Accusation: Sender's ID is not valid")
            return False
        elif self.__accused.is_valid() is False:
            print("Invalid Accusation: Accused's ID is not valid")
            return False
        elif self.__contract.is_valid() is False:
            print("Invalid Accusation: You must provide a valid contract")
            return False
        elif compare_signature(self.__sender.to_dict()["public_key"], self.__signature,
                               self.get_content()) is False:
            print("Invalid Accusation: Signature doesn't match public key")
            return False
        else:
            return True

    def to_dict(self) -> dict:
        """Returns 'Transaction' content on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "signature": self.__signature,
            "accused": self.__accused.to_dict(),
            "contract": self.__contract.to_dict()
        }

    def get_content(self) -> dict:
        """Returns everything except the signature and the hash on a dictionary format"""

        return {
            "sender": self.__sender.to_dict(),
            "accused": self.__accused.to_dict(),
            "contract": self.__contract.to_dict()
        }

    def sign(self) -> None:
        """Adds a signature to the transaction based on it's content"""

        self.__signature = sign(self.__private_key, self.get_content())

    @staticmethod
    def get_random(valid: bool = True) -> dict:
        """Returns a random Accusation with it's corresponding private key"""

        id_info = ID.get_random(valid=valid)
        key, userid = id_info["private_key"], id_info["id"]

        accusation = Accusation(
            import_key(key),
            userid,
            ID.get_random()["id"],
            Contract.get_random()["contract"]
        )

        return {
            "private_key": key,
            "accusation": accusation
        }
