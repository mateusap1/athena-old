import sys
import os
import Crypto.Random
import binascii
import socket
import pickle

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Node_Request import Node_Request
from Node_Response import Node_Response
from config import path_files
from transaction.Contract import Contract
from Request import Request

# https://github.com/adi2381/py-blockchain

HEADER = 10 # The bytes size of the length message
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MAXIMUM_CONNECTIONS = 1000
SERVER = "192.168.1.104"
PORT = 5050
ADDR = (SERVER, PORT)


class Wallet:

    def __init__(self, path = None):
        self.private_key = None
        self.public_key = None
        self.create_keys()

        if path is None:
            self.path = path_files["wallet_path"] + f"/wallet_{self.public_key[:5]}.ath"
        else:
            self.path = path

        self.save()
    
    def save(self):
        with open(self.path, "wb") as wallet_file:
            pickle.dump(self, wallet_file)

    def create_keys(self):
        """Create a new pair of private and public keys"""
        private_key, public_key = Wallet.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def sign_transaction(self, transaction):
        """Sign a transaction and return the signature"""
        # RSA is a cryptography algorithm
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new(str(transaction.get_content()).encode('utf8'))
        signature = signer.sign(h)

        # binascii.hexlify is used to convert binary data to hexadecimal representation
        transaction.sign(binascii.hexlify(signature).decode('ascii'))

    def connect_node(self, node_addr):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(node_addr)

    def send_request(self, command, params):
        message = pickle.dumps(Node_Request(command, params))
        # message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            obj = self.client.recv(msg_length)
            response = pickle.loads(obj)
            if response and response.success:
                return response
            else:
                print(response.message)
        
        return None
    
    def disconnect(self):
        self.send_request("!disconnect", {})

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(str(transaction.get_content()).encode('utf8'))

        return verifier.verify(h, binascii.unhexlify(transaction.signature))
    
    @staticmethod
    def generate_keys():
        """Generating a new pair of private and public key"""

        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()

        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

if __name__ == "__main__":
    # TODO: Discover why the request is failing

    wallet = Wallet()
    wallet.connect_node(ADDR)
    response = wallet.send_request("!get_chain", {})
    if response:
        print("!get_chain")
        print(response.content)
        print(response.message)
    
    response = wallet.send_request("!is_chain_valid", {})
    if response:
        print("!is_chain_valid")
        print(response.content)
        print(response.message)
    
    contract = Contract(
        sender = wallet.public_key, 
        fine = 100,
        rules = ["NAP"],
        judges = ["Calvin", "Luther", "Knox"],
        signatures = []
    )

    contract.sign(wallet.private_key)
    wallet.sign_transaction(contract)

    for i in range(102):
        response = wallet.send_request("!send_transaction", {"transaction": contract})

    if response:
        print("!send_transaction (x102)")
        print(response.content)
        print(response.message)
    
    
    response = wallet.send_request("!is_chain_valid", {})
    if response:
        print("!is_chain_valid")
        print(response.content)
        print(response.message)

    response = wallet.send_request("!get_chain", {})
    if response:
        print("!get_chain")
        print(response.content)
        print(response.message)
    
    request = Request(wallet.public_key, [wallet.public_key], "!!sign_contract", {"contract": contract})
    request.hash()
    wallet.sign_transaction(request)
    print(request.signature)
    response = wallet.send_request("!send_request", {"request": request})
    if response:
        print("!send_request")
        print(response.content)
        print(response.message)

    response = wallet.send_request("!disconnect", {})
    