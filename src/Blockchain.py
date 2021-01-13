import datetime
import hashlib
import json
import requests
import pickle

from uuid import uuid4
from urllib.parse import urlparse

from Block import Block
from config import config


class Blockchain(object):

    def __init__(self):
        self.transactions = []
        self.chain = []
        self.create_block(proof = 1, previous_hash = "0") # Genesis block
        self.nodes = set()
        self.mine_delay = 120 # Interval in seconds between the creation of two blocks that should be aproached
        self.difficulty = 4 # The number of leading zeros necessary to the hash

        # Creating file where the blockchain object will be stored
        with open(f"{config['blockchain_path']}/blockchain.djs", "wb") as blockchain_file:
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

        # Saving recent version of the blockchain
        with open(f"{config['blockchain_path']}/blockchain.djs", "wb") as blockchain_file:
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
        
            with open(f"{config['blockchain_path']}/blockchain.djs", "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)

        print(self.difficulty)
        return self.difficulty
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        difficulty = self.get_mining_difficulty()

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:difficulty] == "0" * difficulty:
                print(hash_operation)
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        difficulty = self.get_mining_difficulty()

        while block_index < len(chain):
            block = chain[block_index]

            if block.previous_hash != previous_block.get_hash():
                return False
            
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:difficulty] != "0" * difficulty:
                return False
            
            previous_block = block
            block_index += 1
        
        return True
    
    def add_transaction(self, transaction_type, data):
        self.transactions.append({
            "transaction_type": transaction_type,
            "data": data
        })

        with open(f"{config['blockchain_path']}/blockchain.djs", "wb") as blockchain_file:
            pickle.dump(self, blockchain_file)

        previous_block = self.get_previous_block()

        return previous_block.index + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

        with open(f"{config['blockchain_path']}/blockchain.djs", "wb") as blockchain_file:
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

            with open(f"{config['blockchain_path']}//blockchain.djs", "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)

            return True
        
        return False
    
    def get_json(self):
        return [block.get_dict() for block in self.chain]
    
    # Transforming json chain into blockchain
    @staticmethod
    def json_to_object(chain):
        return [Block.dict_to_object(json.loads(block)) for block in chain]


