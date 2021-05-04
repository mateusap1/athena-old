import sys
import json
import hashlib
import binascii
import random
import datetime
import requests
import Crypto.Random

from uuid import uuid4
from urllib.parse import urlparse

from collections import Counter

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler

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

            print(
                "Invalid transaction: Transaction has a different type than the expected")
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

        types = {
            Contract: "contract",
            Accusation: "accusation",
            Appeal: "appeal",
            Verdict: "verdict"
        }

        transaction["date"] = str(datetime.datetime.now(datetime.timezone.utc))
        transaction["type"] = types[_type]
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

    def connect_nodes(self, nodes: list) -> None:
        """Connect nodes that weren't connected before"""

        for node in nodes:
            if not Counter(node.keys()) == Counter(["ip", "port"]):
                raise ValueError(
                    "Node must contain two arguments: \"ip\" and \"port\"")
            elif not node in self.__info["connected_nodes"]:
                if not isinstance(node["ip"], str):
                    raise TypeError("Node ip must be of type \"str\"")
                elif not isinstance(node["port"], int):
                    raise TypeError("Node port must be of type \"int\"")

                self.__info["connected_nodes"].append(node)

        self.save()

    def synchronize(self):
        for node in self.__info["connected_nodes"]:
            address = f"{node['ip']}:{str(node['port'])}"

            r = requests.get(f"http://{address}/get_transactions")
            if r.status_code != 200:
                continue

            transactions = r.json()["transactions"]

            for pubkey, transactions in transactions.items():
                if not pubkey in self.__info["transactions"]:
                    self.__info["transactions"][pubkey] = []

                for transaction in transactions:
                    temp = {
                        "content": transaction["content"],
                        "receivers": transaction["receivers"]
                    }

                    types = {
                        "contract": Contract,
                        "accusation": Accusation,
                        "verdict": Verdict,
                        "appeal": Appeal
                    }

                    if not self.is_transaction_valid(temp, types[transaction["type"]]):
                        continue
                    if transaction in self.__info["transactions"][pubkey]:
                        continue

                    self.__info["transactions"][pubkey].append(transaction)

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


app = Flask(__name__)
node = Node()


def cycle():
    print("Executing cycle...")
    node.remove_outdated_transactions()
    node.synchronize()
    print("Cycle ended")


def start():
    scheduler = APScheduler()
    scheduler.add_job(
        func=cycle,
        args=[],
        trigger='interval',
        id='job',
        seconds=30
    )
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)


@app.route('/send_contract', methods=['POST'])
def send_contract():
    data = request.get_json()
    success = node.send_transaction(data, Contract)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400


@app.route('/send_accusation', methods=['POST'])
def send_accusation():
    data = request.get_json()
    success = node.send_transaction(data, Accusation)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400


@app.route('/send_verdict', methods=['POST'])
def send_verdict():
    data = request.get_json()
    success = node.send_transaction(data, Verdict)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400


@app.route('/send_appeal', methods=['POST'])
def send_appeal():
    data = request.get_json()
    success = node.send_transaction(data, Appeal)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    return jsonify({
        "success": True,
        "transactions": node.get_transactions()
    })


@app.route('/random_transaction/<string:transaction_type>/', methods=['GET'])
def random_transaction(transaction_type: str):
    # ! This is here for debugging purposes only. It should be soon removed

    types = {
        "contract": Contract,
        "accusation": Accusation,
        "verdict": Verdict,
        "appeal": Appeal
    }

    if not transaction_type in types:
        return jsonify({
            "success": False,
            "message": "Transaction not found"
        }), 404

    t = types[transaction_type].get_random()

    return jsonify({
        "success": True,
        "content": t[transaction_type].to_dict()
    }), 200


@app.route('/random_id', methods=['GET'])
def random_id():
    # ! This is here for debugging purposes only. It should be soon removed

    _id = ID.get_random()
    return jsonify({
        "success": True,
        "content": _id["id"].to_dict()
    }), 200


if __name__ == '__main__':
    start()
