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

from Node_Request import Node_Request
from Node_Response import Node_Response

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract
from transaction.Transaction import Transaction

from Request import Request
from Blockchain import Blockchain
from Wallet import Wallet
from config import path_files
from utils.transaction_utils import compare_signature


BLOCKCHAIN_PATH = path_files["blockchain_path"] + "/blockchain.ath"
WALLET_PATH = path_files["wallet_path"] + "/node_wallet.ath"
HEADER = 10 # The bytes size of the length message
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.1.104"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"
MAX_CONNECTIONS = 1000
MAX_TRANSACTIONS = 100


class Node(object):

    def __init__(self, blockchain = None, wallet = None):
        self.blockchain = blockchain
        self.wallet = wallet
        self.load()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.running = False

        self.connections = []
        self.commands = {
            "!get_chain": self.get_chain,
            "!is_chain_valid": self.is_chain_valid,
            "!send_transaction": self.send_transaction,
            "!send_request": self.send_request,
            "!connect_nodes": self.connect_nodes,
            "!replace_chain": self.replace_chain
        }
    
    def load(self):
        """Loading essential components of the blockchain"""

        if self.blockchain is None:
            try:
                with open(BLOCKCHAIN_PATH, "rb") as blockchain_file:
                    self.blockchain = pickle.load(blockchain_file)
            except IOError:
                self.blockchain = Blockchain()
        
        if self.wallet is None:
            try:
                with open(WALLET_PATH, "rb") as wallet_file:
                    self.wallet = pickle.load(wallet_file)
            except IOError:
                self.wallet = Wallet(WALLET_PATH)
    
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        self.connections.append(addr)
        while addr in self.connections:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                request = pickle.loads(msg)

                if isinstance(request, Node_Request):
                    print(f"[{addr}] {request.command}")

                    if request.command == DISCONNECT_MESSAGE:
                        response = self.disconnect(addr)
                    else:
                        response = self.handle_request(request)
                    
                    bytes_response = pickle.dumps(response)
                    rsp_length = len(bytes_response)
                    send_length = str(rsp_length).encode(FORMAT)
                    send_length += b' ' * (HEADER - len(send_length))
                    conn.send(send_length)

                    conn.send(bytes_response)

        conn.close()
    
    def disconnect(self, addr):
        self.connections.remove(addr)

        return Node_Response(True, None, f"[DISCONNECTING] Server disconnected on {addr}")
    
    def disconnect_all(self):
        self.connections = []
    
    def start(self):
        self.server.listen(MAX_CONNECTIONS)
        print(f"[LISTENING] Server is listening on {SERVER}")

        self.running = True
        while self.running:
            conn, addr = self.server.accept()
            if not addr in self.connections:
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            
    def stop(self):
        self.running = False
    
    def handle_request(self, request):
        command = request.command
        params = request.params

        if command in self.commands:
            response = self.commands[command](**params)
        else:
            response = Node_Response(success = False, content = None, message = "[ERROR] Command not found")

        return response
    
    def mine_block(self):
        print("[SERVER] Starting block mining")
        block = self.blockchain.create_block()

        return Node_Response(success = True, content = block, message = "Block mined successfully")
    
    def get_chain(self):
        chain = self.blockchain.chain

        content = {
            "chain": chain,
            "length": len(chain)
        }
        response = Node_Response(success = True, content = content, message = "Everything went fine")

        return response
    
    def is_chain_valid(self):
        if Blockchain.is_chain_valid(self.blockchain):
            return Node_Response(success = True, content = True, message = "[Success] The chain is valid")
        else:
            return Node_Response(success = True, content = False, message = "[Success] The chain is not valid")
    
    def send_transaction(self, transaction):
        if len(self.blockchain.transactions) > MAX_TRANSACTIONS:
            self.mine_block()
            print("[SERVER] Block mined successfuly")

        if transaction.is_valid():
            index = self.blockchain.add_transaction(transaction)
            return Node_Response(True, index, "[Success] The transaction was added to the list")
        
        return Node_Response(False, None, "[ERROR] The transaction is not valid")
        
    def send_request(self, request):
        if request.signature is None:
            return Node_Response(False, None, "[ERROR] The transaction signature is not valid")

        if compare_signature(
            request.sender, 
            request.signature, 
            str(request.get_content())
        ) is False:
            return Node_Response(False, None, "[ERROR] The request signature is not valid")
        
        if len(request.receivers) == 0:
            return Node_Response(False, None, "[ERROR] There must have at least one receiver")
        
        if request.hash_value is None:
            return Node_Response(False, None, "[ERROR] The request was not hashed correctly")
        
        encoded_request = json.dumps(request.get_content(), sort_keys = True).encode()
        hash_value = hashlib.sha256(encoded_request).hexdigest()

        if not hash_value == request.hash_value:
            return Node_Response(False, None, "[ERROR] The request was not hashed correctly")
        
        request_date = request.timestamp
        current_date = datetime.datetime.now(datetime.timezone.utc)
        
        if request_date > current_date:
            return Node_Response(False, None, "[ERROR] Invalid timestamp")
        
        if request_date + datetime.timedelta(hours = 3) < current_date:
            return Node_Response(False, None, "[ERROR] Invalid timestamp")

        self.blockchain.add_request(request)

        return Node_Response(True, len(self.blockchain.temp_requests), "[SUCCESS] The request was sent with success")

    def connect_nodes(self, nodes):
        for node in nodes:
            self.blockchain.add_node(node)
        
        return Node_Response(True, self.blockchain.nodes, "[Success] Nodes connected successfully")
    
    def replace_chain(self):
        is_chain_replaced = self.blockchain.replace_chain(self.wallet)

        if is_chain_replaced:
            response = Node_Response(True, self.blockchain.chain, "[Success] The chain was replaced by a longer one")
        else:
            response = Node_Response(True, self.blockchain.chain, "[Success] The chain was already the longest")
        
        return response

if __name__ == "__main__":
    node = Node()
    try:
        node.start()
    except KeyboardInterrupt:
        print("[SERVER] Stoping...")
        node.disconnect_all()
        node.stop()