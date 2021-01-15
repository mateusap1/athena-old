import json
import requests
import pickle

from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse

from Blockchain import Blockchain
from Wallet.Wallet import Wallet
from config import config


# Initializing the web app
app = Flask(__name__)

# Initializing the Blockchain
try:
    with open(f"{config['blockchain_path']}/blockchain.ath", "rb") as blockchain_file:
        blockchain = pickle.load(blockchain_file)
except IOError:
    blockchain = Blockchain()

# Creating an address to the node
node_address = str(uuid4()).replace("-", "")

@app.route("/mine_block", methods = ["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block.proof
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block.get_hash()

    block = blockchain.create_block(proof, previous_hash)
    response = {"message": "Block mined successfully!", 
                **block.get_dict()}

    return jsonify(response), 200

@app.route("/get_chain", methods = ["GET"])
def get_chain():
    response = {"chain": blockchain.get_dict_list(),
                "length": len(blockchain.chain)}

    return jsonify(response), 200

@app.route("/is_valid", methods = ["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)

    if is_valid:
        response = {"message": "The chain is valid."}
    else:
        response = {"message": "The chain is not valid."}

    return jsonify(response), 200

@app.route("/send_transaction", methods = ["POST"])
def send_transaction():
    json_file = request.get_json()
    transaction_keys = ["sender", "transaction_type", "data", "fee", "signature"]

    # Checking if all keys were given
    if not all(key in json_file for key in transaction_keys):
        return "Missing transactions keys!", 400
    
    # Adding a transaction in the blockchain with it correspondent paramaters
    block_index = blockchain.add_transaction(
        json_file["sender"],
        json_file["transaction_type"], 
        json_file["data"],
        json_file["fee"],
        json_file["signature"]
    )

    if block_index:
        response = {
            "message": f"The transaction will be added to the block with index {block_index}.",
            "block_index": block_index
        }

        return jsonify(response), 200

    else:
        response = {
            "message": f"The transaction failed. Check your paramaters and try again."
        }
    
        return jsonify(response), 400

@app.route("/connect_node", methods = ["POST"])
def connect_node():
    json = request.get_json()
    nodes = json.get("nodes")

    if nodes is None:
        return "No node given!", 400
    
    for node in nodes:
        blockchain.add_node(node)
    
    response = {"message": "The nodes were successfully connected.",
                "total_nodes": list(blockchain.nodes)}
    
    return jsonify(response), 200

@app.route("/replace_chain", methods = ["GET"])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()

    if is_chain_replaced:
        response = {"message": "The nodes had a different chain so it was replaced by the longest one.",
                    "new_chain": blockchain.get_dict_list()}
    else:
        response = {"message": "The chain is the largest one.",
                    "actual_chain": blockchain.get_dict_list()}

    return jsonify(response), 200

def run_server(host, port):
    app.run(host = host, port = port)

if __name__ == "__main__":
    run_server(host = "0.0.0.0", port = 5000)