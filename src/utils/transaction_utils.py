from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii


def compare_signature(public_key: str, signature: str, content: str) -> bool:
    public_key = RSA.importKey(binascii.unhexlify(public_key))
    verifier = PKCS1_v1_5.new(public_key)
    h = SHA256.new(content.encode('utf8'))

    return verifier.verify(h, binascii.unhexlify(signature))