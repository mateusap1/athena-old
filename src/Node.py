import json
import socket
import threading
import pickle
import hashlib
import binascii
import datetime
import Crypto.Random

from uuid import uuid4
from urllib.parse import urlparse

from collections import Counter

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract
from transaction.Transaction import Transaction

from Account import Account
from config import path_files, id_config, node_config
from utils import compare_signature, verify_hash


NODE_PATH = path_files["node_path"] + "/info.json"
MAX_TRANSACTIONS = 100
HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]
TRANSACTIONS_DAYLIMIT = node_config["transactions_daylimit"]


"""
How info should look like ->
{
    "connected_nodes": [
        {"ip": "192.168.0.1", "port": "6969"},
        {"ip": "192.168.0.11", "port": "69420"}
    ],
    "transactions": [
        {
            "type": "contract",
            "content": {...},
            "receivers": [...],
            "date": "2021-04-15 21:34:31.991790+00:00"
        }
    ]
}
"""

"""
How ID should look like ->
{
    "username": "Mateus Oliveira",
    "public_key": "5ed0cd...f91a98",
    "nonce": 228289,
    "creation_date": "2021-04-15 21:34:31.991790+00:00",
    "hash_value": "00000e...9b3b75"
}
"""


class Node(object):

    def __init__(self, info: dict = None):
        self._info = info
        self.load()

    def load(self) -> None:
        """Loads essential components of the node"""

        if self._info is None:
            try:
                with open(NODE_PATH, "r") as f:
                    self._info = json.load(f)
            except IOError:
                self._info = {"connected_nodes": [], "transactions": []}

                self.save()

    def save(self) -> None:
        """Saves the changes into a JSON file"""

        with open(NODE_PATH, "w") as f:
            self._info = json.dump(self._info, f)

    def get_transactions(self) -> list:
        """Returns all transactions stored inside this node"""

        return self._info["transactions"]

    def is_transaction_valid(self, transaction: dict) -> bool:
        """Verfies if a transaction is valid or not"""

        required_keys = ["type", "content", "receivers"]

        if Counter(transaction.keys()) != Counter(required_keys):
            # If, doesn't matter the order, the keys are not all
            # the same as the expected ones, return False

            return False

        tr_type = transaction["type"]
        tr_content = transaction["content"]
        tr_receivers = transaction["receivers"]

        expected_obj_types = {
            "tr_type": str,
            "tr_content": dict,
            "tr_receivers": list
        }

        if any([not isinstance(value, expected_obj_types[key]) for key, value in transaction.items()]):
            # Returns false if any of the transaction values
            # have a different type other than the expected

            return False

        valid_transaction = ["Contract", "Accusation", "Verdict", "Appeal"]

        if not tr_type in valid_transaction:
            return False

        transaction_types = {
            "Contract": Contract,
            "Accusation": Accusation,
            "Verdict": Verdict,
            "Appeal": None  # TODO: Make this transaction
        }

        try:  # Tries creating a transaction object with the given dict
            transaction = transaction_types[tr_type](**tr_content)

            if transaction.is_valid() is False:
                return False

        except TypeError:
            return False

        for userid in tr_receivers:
            if self.is_id_valid(userid) is False:
                return False

        return True

    def send_transaction(self, transaction: dict) -> bool:
        """Stores the transaction sent if it's valid and has valid IDs"""

        if len(self._info["transactions"]) == MAX_TRANSACTIONS:
            # If the limit of transactions was exceeded, don't add it

            return False

        if self.is_transaction_valid(transaction) is False:
            return False

        transaction["date"] = str(datetime.datetime.now(datetime.timezone.utc))
        self._info["transactions"].append(transaction)

        self.save()

        return True

    def connect_nodes(self, nodes: dict) -> None:
        """Connect nodes that weren't connected before"""

        for node in nodes:
            if not Counter(nodes.keys()) == Counter(["ip", "port"]):
                raise ValueError(
                    "Node must contain two arguments: \"ip\" and \"port\"")
            elif not node in self._info["connected_nodes"]:
                if not isinstance(node["ip"], str):
                    raise TypeError("Node ip must be of type \"str\"")
                elif not isinstance(node["port"], int):
                    raise TypeError("Node port must be of type \"int\"")

                self._info["connected_nodes"].append(node)

        self.save()

    def remove_outdated_transactions(self):
        """Removes any transactions that were added more than N days ago, 
        where N is the transactions day limit"""

        date_limit = datetime.datetime.now(datetime.timezone.utc) - \
            datetime.timedelta(days=TRANSACTIONS_DAYLIMIT)

        self._info["transactions"] = list(filter(
            lambda x: datetime.datetime.strptime(
                x["date"], "%Y-%m-%d %H:%M:%S.%f") > date_limit,
            self._info["transactions"]
        ))

        self.save()


if __name__ == "__main__":
    node = Node()
    account = Account("password")

    myid = account.info["ID"]
    print(node.is_id_valid(myid))
