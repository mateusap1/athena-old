import datetime
import hashlib
import json
import requests
import pickle
import sys

from uuid import uuid4
from urllib.parse import urlparse
from Block import Block
from Wallet import Wallet

from config import path_files


BLOCKCHAIN_PATH = path_files["blockchain_path"] + "/blockchain.ath"


class Blockchain(object):

    def __init__(self, store_object=True):
        self.store_object = store_object

        self.transactions = []
        self.temp_requests = []
        self.temp_responses = []
        self.chain = []
        self.nodes = set()

        # The number of leading zeros necessary to the hash
        self.difficulty = 4

        # Create genesis block
        self.create_block()
        self.save()
    
    def save(self):
        if self.store_object:
            with open(BLOCKCHAIN_PATH, "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)

    def create_block(self):
        """Creates and mines a block with the current transactions"""

        if len(self.chain) == 0:
            previous_hash = "0"
        else:
            previous_hash = self.get_previous_block().hash_value

        block = Block(
            index = len(self.chain) + 1,
            transactions = self.transactions,
            previous_hash = previous_hash
        )
        block.hash()

        self.transactions = []
        self.chain.append(block)

        if self.store_object:
            # Saving recent version of the blockchain
            with open(BLOCKCHAIN_PATH, "wb") as blockchain_file:
                pickle.dump(self, blockchain_file)

        return block

    def get_previous_block(self):
        if len(self.chain) == 0:
            return None
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save()

        previous_block = self.get_previous_block()

        return previous_block.index + 1

    def add_request(self, request):
        self.temp_requests.append(request)
        self.save()
    
    def add_response(self, response):
        self.temp_responses.append(response)
        self.save()

    def add_node(self, address):
        # Validation
        if not isinstance(address, tuple):
            raise Exception("[ERROR] Address must be of type tuple")
        if not len(address) == 2:
            raise Exception("[ERROR] Address must have length of 2")
        if not isinstance(address[0], str):
            raise Exception("[ERROR] Addresses first element must be of typestring")
        if not isinstance(address[1], int):
            raise Exception("[ERROR] Addresses second element must be of type int")

        self.nodes.add(address)
        self.save()

    def remove_node(self, node):
        self.nodes.remove(node)
        self.save()

    def replace_chain(self, wallet):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            if isinstance(node, tuple):
                wallet.connect_node(node)
                response = wallet.send_request("!get_chain", {})

                if response and response.success == True:
                    chain = response.content["chain"]
                    length = response.content["length"]

                    if length > max_length and Blockchain.is_chain_valid(chain):
                        longest_chain = chain
                        max_length = length

        if longest_chain:
            self.chain = longest_chain
            self.save()

            return True

        return False

    def get_dict_list(self):
        return [block.to_dict() for block in self.chain]

    @staticmethod
    def is_chain_valid(blockchain):
        for block in blockchain.chain:
            for transaction in block.transactions:
                if transaction.is_valid() is False:
                    return False
            
            encoded_block = json.dumps(block.get_content(), sort_keys = True).encode()
            current_hash = hashlib.sha256(encoded_block).hexdigest()

            if current_hash != block.hash_value:
                return False
            
            if block.hash_value[:blockchain.difficulty] != "0" * blockchain.difficulty:
                return False

        return True

    @staticmethod
    def json_to_object(chain):
        return [Block.dict_to_object(json.loads(block)) for block in chain]
