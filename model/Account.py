import sys
import os
import Crypto.Random
import binascii
import socket
import json
import datetime
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from config import path_files, id_config
from utils import hash_content, create_key, parse_key


HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]


class UnspecifiedInformation(Exception):
    pass


class Account:
    """Used to send or receive any transactions"""

    def __init__(self, password: str, username: str = None):
        self.__password = password
        self.__username = username

        self.__id = None
        self.__node = {}
        self.__transactions = []

        self.key_path = path_files["account_path"] + "/private_key.pem"
        self.info_path = path_files["account_path"] + f"/info.json"

        self.create_keys()
        self.create_id()
    
    def save(self):
        info = {
            "id": self.__id,
            "node": self.__node,
            "transactions": self.__transactions
        }

        with open(self.info_path, 'w') as f:
            json.dump(info, f)

    def create_keys(self):
        """Create a new pair of private and public keys"""
        try:
            # If we've already created a private key before, import it
            # Otherwise, create it

            with open(self.key_path, "r") as f:
                private_key = RSA.import_key(
                    f.read(), passphrase=self.__password)
                public_key = private_key.publickey()
        except IOError:
            private_key = create_key()
            public_key = private_key.publickey()

            with open(self.key_path, "wb") as f:
                f.write(private_key.export_key(
                    "PEM", passphrase=self.__password))

        self.__private_key = parse_key(private_key)
        self.__public_key = parse_key(public_key)

    def create_id(self):
        """Creates an ID if there isn't one already"""

        try:
            with open(self.info_path) as f:
                self.__info = json.load(f)
        except IOError:
            if self.__username is None:
                raise UnspecifiedInformation("Username not provided")

            content = {
                "username": self.__username,
                "public_key": self.__public_key
            }

            content = hash_content(content, HASH_DIFFICULTY, 10**6)

            info = {
                "id": content,
                "node": self.__node,
                "transactions": self.__transactions
            }

            with open(self.info_path, 'w') as f:
                json.dump(info, f)

    def connect_node(self, node: dict):
        if not ("ip" in node and "port" in node):
            print("Error: node must be a dictionary with an IP and a PORT")
            return None

        self.__node = node


if __name__ == "__main__":
    account = Account("password", username = "Mateus")
