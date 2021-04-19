from __future__ import annotations

from utils import hash_content, random_word, create_key, parse_key, verify_hash
from config import id_config

from collections import Counter

import random


HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]


class ID(object):

    def __init__(self, username: str, public_key: str, nonce: int = None,
                 timestamp: str = None, hash_value: str = None):

        if not isinstance(username, str):
            raise TypeError("\"username\" must be of type str")
        elif not isinstance(public_key, str):
            raise TypeError("\"public_key\" must be of type str")
        elif not (nonce is None or isinstance(nonce, int)):
            raise TypeError("\"nonce\" must be of type int")
        elif not (timestamp is None or isinstance(timestamp, str)):
            raise TypeError("\"timestamp\" must be of type str")
        elif not (hash_value is None or isinstance(hash_value, str)):
            raise TypeError("\"hash_value\" must be of type str")

        self.__username = username
        self.__public_key = public_key

        if all([i is None for i in [nonce, timestamp, hash_value]]):
            # If all extra values are None, hash the content

            self.__hash()
        elif None in [nonce, timestamp, hash_value]:
            # If one of the extra values has a value, all must have,
            # otherwise raise an exception

            raise ValueError(
                "\"nonce\", \"timestamp\" and \"hash_value\" are dependent, " +
                "either all of them have a value or none of them do.")
        else:
            self.__nonce = nonce
            self.__timestamp = timestamp
            self.__hash_value = hash_value

    def __hash(self) -> None:
        content = {
            "username": self.__username,
            "public_key": self.__public_key
        }

        content = hash_content(content, HASH_DIFFICULTY, 10**6)

        self.__nonce = content["nonce"]
        self.__timestamp = content["timestamp"]
        self.__hash_value = content["hash_value"]

    def to_dict(self) -> dict:
        """Returns all class paramaters in a dictionary form"""

        return {
            "username": self.__username,
            "public_key": self.__public_key,
            "nonce": self.__nonce,
            "timestamp": self.__timestamp,
            "hash_value": self.__hash_value
        }

    def get_content(self) -> dict:
        """Returns only the class paramaters that can be hashed"""

        return {
            "username": self.__username,
            "public_key": self.__public_key
        }

    def is_valid(self) -> bool:
        """Verfies if ID is valid or not"""

        if len(self.__username) > USERNAME_LIMIT:
            return False

        if self.__nonce > NONCE_LIMIT:
            return False

        content = {
            "username": self.__username,
            "public_key": self.__public_key,
            "nonce": self.__nonce,
            "timestamp": self.__timestamp,
        }

        if len(self.__hash_value) < 6:
            return False

        if self.__hash_value[:HASH_DIFFICULTY] != "0" * HASH_DIFFICULTY:
            return False

        if verify_hash(content, self.__hash_value) is False:
            return False

        return True

    @staticmethod
    def is_id_valid(userid: dict) -> bool:
        """Verfies if a dictionary version of an ID is valid or not"""

        required_keys = ["username", "public_key",
                         "nonce", "timestamp", "hash_value"]

        if Counter(userid.keys()) != Counter(required_keys):
            # If, doesn't matter the order, the keys are not all
            # the same as the expected ones, return False

            return False

        expected_types = {
            "username": str,
            "public_key": str,
            "nonce": int,
            "timestamp": str,
            "hash_value": str
        }

        if any([not isinstance(value, expected_types[key]) for key, value in userid.items()]):
            # Returns false if any of the id values have a
            # different type other than the expected

            return False

        id = ID(**userid)

        if id.is_valid() is False:
            return False

        return True

    @staticmethod
    def get_random(valid: bool = True) -> dict:
        """Returns a random ID with it's corresponding private key"""

        key = create_key()
        pubkey = parse_key(key.publickey())
        username = random_word(random.randint(1, USERNAME_LIMIT))

        if valid is False:
            username = "A" * (USERNAME_LIMIT+1)

        return {
            "private_key": parse_key(key),
            "id": ID(username, pubkey)
        }
