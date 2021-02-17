import hashlib
import json

from abc import ABC, abstractmethod


class Transaction(ABC):

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def get_content(self) -> dict:
        pass

    def sign(self, signature):
        self.signature = signature

    @staticmethod
    def dict_to_object(dict_version):
        return Transaction(**dict_version)

    @staticmethod
    def get_dict_list(transactions: list) -> list:
        return [transaction.get_dict() for transaction in transactions]
