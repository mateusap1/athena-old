import json
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

from transaction.Appeal import Appeal
from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract
from transaction.Transaction import Transaction

from Account import Account
from identity import ID
from config import path_files, id_config, node_config
from utils import compare_signature, verify_hash


NODE_PATH = path_files["node_path"] + "/info.json"
HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]
TRANSACTIONS_LIMIT = node_config["transactions_limit"]
MAX_TRANSACTIONS = node_config["max_transactions"]
TRANSACTION_EXPIRE_DAYS = node_config["transactions_expire_days"]


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
        self.__info = info
        self.load()

    def load(self) -> None:
        """Loads essential components of the node"""

        if self.__info is None:
            try:
                with open(NODE_PATH, "r") as f:
                    self.__info = json.load(f)
            except IOError:
                self.__info = {"connected_nodes": [], "transactions": {}}

                self.save()

    def save(self) -> None:
        """Saves the changes into a JSON file"""

        with open(NODE_PATH, "w") as f:
            json.dump(self.__info, f)

    def get_transactions(self) -> list:
        """Returns all transactions stored inside this node"""

        return self.__info["transactions"]

    def is_transaction_valid(self, transaction: dict, _type: object) -> bool:
        """Verfies if a transaction is valid or not"""

        required_keys = ["content", "receivers"]

        if Counter(transaction.keys()) != Counter(required_keys):
            # If, doesn't matter the order, the keys are not all
            # the same as the expected ones, return False

            print("Invalid transaction: Keys don't match")
            return False

        tr_content = transaction["content"]
        tr_receivers = transaction["receivers"]

        expected_obj_types = {
            "content": dict,
            "receivers": list
        }

        if any([not isinstance(value, expected_obj_types[key]) for key, value in transaction.items()]):
            # Returns false if any of the transaction values
            # have a different type other than the expected

            print("Invalid transaction: Transaction has a different type than the expected")
            return False
        
        t = _type.import_dict(transaction["content"])
        if t is None or t.is_valid() is False:
            print("Invalid transaction")
            return False

        for userid in tr_receivers:
            try:
                if ID(**userid).is_valid() is False:
                    return False
            except TypeError as e:
                print(e)
                print("Invalid transaction: Invalid judge ID")
                return False

        return True

    def send_transaction(self, transaction: dict, _type: object) -> bool:
        """Stores the transaction sent if it's valid and has valid IDs"""

        if len(self.__info["transactions"]) == MAX_TRANSACTIONS:
            print("Error while adding transaction: Limit of transactions exceeded")
            return False
        
        if self.is_transaction_valid(transaction, _type) is False:
            print("Error while adding transaction: Invalid transaction")
            return False

        transaction["date"] = str(datetime.datetime.now(datetime.timezone.utc))
        sender = transaction["content"]["sender"]["public_key"]

        if sender in self.__info["transactions"]:
            if len(self.__info["transactions"][sender]) == TRANSACTIONS_LIMIT:
                print("Error while adding transaction: " + 
                      "Account exceeded it's transactions limit")
                return False

            self.__info["transactions"][sender].append(transaction)
        else:
            self.__info["transactions"][sender] = [transaction]

        self.save()

        return True

    def connect_nodes(self, nodes: dict) -> None:
        """Connect nodes that weren't connected before"""

        for node in nodes:
            if not Counter(nodes.keys()) == Counter(["ip", "port"]):
                raise ValueError(
                    "Node must contain two arguments: \"ip\" and \"port\"")
            elif not node in self.__info["connected_nodes"]:
                if not isinstance(node["ip"], str):
                    raise TypeError("Node ip must be of type \"str\"")
                elif not isinstance(node["port"], int):
                    raise TypeError("Node port must be of type \"int\"")

                self.__info["connected_nodes"].append(node)

        self.save()

    def remove_outdated_transactions(self):
        """Removes any transactions that were added more than N days ago, 
        where N is the transactions day limit"""

        date_limit = datetime.datetime.now(datetime.timezone.utc) - \
            datetime.timedelta(days=TRANSACTION_EXPIRE_DAYS)
        
        for key, value in self.__info["transactions"].items():
            self.__info["transactions"][key] = list(filter(
                lambda x: datetime.datetime.strptime(
                    x["date"], 
                    "%Y-%m-%d %H:%M:%S.%f%z"
                ) > date_limit,
                value
            ))

        self.save()


if __name__ == "__main__":
    node = Node()
    account = Account("password")

    myid = account.info["ID"]
    print(node.is_id_valid(myid))
