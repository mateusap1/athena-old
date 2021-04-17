from __future__ import annotations

from abc import ABC, abstractmethod
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey.RSA import RsaKey

import hashlib
import json
import binascii


class Transaction(ABC):

    @abstractmethod
    def sign(self) -> None:
        """Adds a signature to the transaction based on it's content"""
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """Verifies the validation of a transaction"""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Transforms the object into a dictionary"""
        pass

    @abstractmethod
    def get_content(self) -> dict:
        """Return a dicitionary version of this transaction 
        containing only the essential information"""
        pass

    @staticmethod
    def dict_to_object(dict_version: dict) -> Transaction:
        return Transaction(**dict_version)

    @staticmethod
    def get_dict_list(transactions: list) -> list:
        return [transaction.get_dict() for transaction in transactions]
