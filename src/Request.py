import json
import hashlib
import datetime

from transaction.Transaction import Transaction


class Request(object):

    def __init__(self, sender, receivers, command, params):
        self.timestamp = None
        self.signature = None
        self.hash_value = None
        self.nonce = None

        self.sender = sender
        self.receivers = receivers
        self.command = command
        self.params = params
    
    def hash(self):
        nonce = 0
        current_hash = ""
        while not current_hash[:5] == "0" * 5:
            nonce += 1
            self.timestamp = datetime.datetime.now(datetime.timezone.utc)
            self.nonce = nonce

            encoded_request = json.dumps(self.get_content(), sort_keys = True).encode()
            current_hash = hashlib.sha256(encoded_request).hexdigest()

        self.hash_value = current_hash
        self.nonce = nonce
    
    def sign(self, signature):
        self.signature = signature
    
    def to_dict(self):
        params = {}
        for obj in self.params:
            if isinstance(obj, Transaction):
                params[obj] = self.params[obj].to_dict()

        return {
            "timestamp": str(self.timestamp),
            "hash": self.hash_value,
            "nonce": self.nonce,
            "signature": self.signature,
            "sender": self.sender,
            "receivers": self.receivers,
            "command": self.command,
            "params": params
        }
    
    def get_content(self):
        params = {}
        for obj in self.params:
            if isinstance(obj, Transaction):
                params[obj] = self.params[obj].to_dict()

        return {
            "timestamp": str(self.timestamp),
            "nonce": self.nonce,
            "sender": self.sender,
            "receivers": self.receivers,
            "command": self.command,
            "params": params
        }