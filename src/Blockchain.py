import datetime
import hashlib
import json
import requests
import pickle
import sys

from uuid import uuid4
from urllib.parse import urlparse

from Block import Block
from wallet.Wallet import Wallet
from transaction.Payment import Payment
# from transaction.Transaction import Transaction
from config import config


FILE_NAME = config["file_name"]
FILE_PATH = config['blockchain_path']
FILE_FULL_PATH = f"{FILE_PATH}/{FILE_NAME}"

class Blockchain(object):

    def __init__(self, store_object = True):
        self.store_object = store_object

        self.transactions = []
        self.chain = []
        self.create_block(proof = 1, previous_hash = "0") # Genesis block
        self.nodes = set()
        self.mine_delay = 120 # Interval in seconds between the creation of two blocks that should be aproached
        self.difficulty = 4 # The number of leading zeros necessary to the hash

        if self.store_object:
            # Creating file where the blockchain object will be stored
            with open(FILE_FULL_PATH, "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)
    
    def create_block(self, proof, previous_hash):
        block = Block(
            index = len(self.chain) + 1,
            timestamp = str(datetime.datetime.now()),
            transactions = self.transactions,
            proof = proof,
            previous_hash = previous_hash
        )

        self.transactions = []
        self.chain.append(block)

        if self.store_object:
            # Saving recent version of the blockchain
            with open(FILE_FULL_PATH, "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)

        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def get_mining_difficulty(self):
        if len(self.chain) < 2:
            return self.difficulty
        
        previous_block = self.get_previous_block()
        before_previous_block = self.chain[-2]

        first_block_time = datetime.datetime.strptime(previous_block.timestamp, "%Y-%m-%d %H:%M:%S.%f")
        second_block_time = datetime.datetime.strptime(before_previous_block.timestamp, "%Y-%m-%d %H:%M:%S.%f")
        
        total_time_spent = (first_block_time - second_block_time).total_seconds() # The time that took to mine a new block
        hash_operation = hashlib.sha256(str(previous_block.proof**2 - before_previous_block.proof**2).encode()).hexdigest()

        # Number of leading zeros from the last block checked
        current_difficulty = len(hash_operation) - len(hash_operation.lstrip("0"))

        # If the miners were 16x faster then the ideal time then the difficulty should be improved
        if (float(total_time_spent) * 16) < self.mine_delay:
            self.difficulty = current_difficulty + 1
        
            if self.store_object:
                with open(FILE_FULL_PATH, "wb") as blockchain_file:
                    pickle.dump(self, blockchain_file)

        return self.difficulty
    
    def get_current_reward(self):
        return 100
    
    def proof_of_work(self, previous_proof: int) -> int:
        # TODO: Make the proof of work differ when the timestamp is changed
        if previous_proof > 2 ** 32 or previous_proof < 0:
            raise Exception("previous_proof must be a positive integer with maximum size of 32 bits")

        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:self.difficulty] == "0" * self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        if self.store_object:
            with open(FILE_FULL_PATH, "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)

        previous_block = self.get_previous_block()

        return previous_block.index + 1
    
    def get_balance(self, public_key):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if isinstance(transaction, Payment):
                    if transaction.receiver == public_key:
                        balance += transaction.amount
                    elif transaction.sender == public_key:
                        balance -= transaction.amount
                        balance -= transaction.fee
        
        return balance
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

        if self.store_object:
            with open(FILE_FULL_PATH, "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f"http://{node}/get_chain")

            if response.status_code == 200:
                chain = Blockchain.json_to_object(response.json()["chain"])
                length = response.json()["length"]

                if length > max_length and Blockchain.is_chain_valid(chain):
                    longest_chain = chain
                    max_length = length
        
        if longest_chain:
            self.chain = longest_chain

            if self.store_object:
                with open(f"{config['blockchain_path']}//{FILE_NAME}", "wb") as blockchain_file:
                    pickle.dump(self, blockchain_file)

            return True
        
        return False
    
    def get_dict_list(self):
        return [block.get_dict() for block in self.chain]
    
    @staticmethod
    def json_to_object(chain):
        return [Block.dict_to_object(json.loads(block)) for block in chain]


