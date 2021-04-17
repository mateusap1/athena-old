from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey.RSA import RsaKey

from config import id_config
from collections import Counter

import Crypto.Random
import binascii
import hashlib
import json
import datetime
import random
import string


HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]


def create_key() -> RSA.RsaKey:
    """Creates a random private key"""

    return RSA.generate(1024, Crypto.Random.new().read)


def parse_key(key: RSA.RsaKey) -> str:
    """Returns the string version of a RSA key"""

    return binascii.hexlify(key.exportKey(
        format='DER')).decode('ascii')

def import_key(key: str) -> RSA.RsaKey:
    """Returns the RSA key correspondent to a string version.
    It's the inverse function of parse_key"""

    return RSA.importKey(binascii.unhexlify(key))

def sign(private_key: RsaKey, content: dict) -> None:
    """Returns a signature according to a private key and a content"""

    signer = PKCS1_v1_5.new(private_key)
    encoded_content = json.dumps(content, sort_keys=True).encode()
    h = SHA256.new(encoded_content)
    signature = signer.sign(h)

    return binascii.hexlify(signature).decode('ascii')


def compare_signature(public_key: str, signature: str, content: dict) -> bool:
    """Verifies if the signature is valid"""

    public_key = import_key(public_key)
    verifier = PKCS1_v1_5.new(public_key)
    encoded_content = json.dumps(content, sort_keys=True).encode()
    h = SHA256.new(encoded_content)

    return verifier.verify(h, binascii.unhexlify(signature))


def verify_hash(content: dict, hashing: str) -> bool:
    """Verifies if the hash is valid"""

    encoded_content = json.dumps(content, sort_keys=True).encode()
    hash_value = hashlib.sha256(encoded_content).hexdigest()

    return hash_value == hashing


def hash_content(content: dict, difficulty: int, nonce_limit: int) -> dict:
    """Returns the new dictionary with it's hash containing 
    N leading zeros, where N is the given difficulty"""

    content["nonce"] = 0
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    content["timestamp"] = str(timestamp)
    hash_value = ""

    while not hash_value[:difficulty] == "0" * difficulty:
        content["nonce"] += 1

        if content["nonce"] > nonce_limit:
            timestamp = datetime.datetime.now(
                datetime.timezone.utc)

            content["timestamp"] = str(timestamp)
            content["nonce"] = 0

        encoded_content = json.dumps(content, sort_keys=True).encode()
        hash_value = hashlib.sha256(encoded_content).hexdigest()

    content["hash_value"] = hash_value

    return content


def random_word(length):
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for _ in range(length))
