from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from node import Node

from transaction.Contract import Contract
from transaction.Accusation import Accusation
from transaction.Verdict import Verdict
from transaction.Appeal import Appeal
from identity import ID

import random

app = Flask(__name__)
node = Node()

def cycle():
    print("Executing cycle...")
    node.remove_outdated_transactions()
    print("Cycle ended")

@app.route('/send_contract', methods=['POST'])
def send_contract():
    data = request.get_json()
    success = node.send_transaction(data, Contract)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400

@app.route('/send_accusation', methods=['POST'])
def send_accusation():
    data = request.get_json()
    success = node.send_transaction(data, Accusation)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400

@app.route('/send_verdict', methods=['POST'])
def send_verdict():
    data = request.get_json()
    success = node.send_transaction(data, Verdict)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400

@app.route('/send_appeal', methods=['POST'])
def send_appeal():
    data = request.get_json()
    success = node.send_transaction(data, Appeal)

    if success is True:
        return jsonify({
            "success": True,
            "message": "Transaction added successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid transaction"
        }), 400
    
@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    return jsonify({
        "success": True,
        "transactions": node.get_transactions()
    })

# ! This is here for debugging purposes only. It should be soon removed
@app.route('/random_transaction/<string:transaction_type>/', methods=['GET'])
def random_transaction(transaction_type: str):
    types = {
        "contract": Contract,
        "accusation": Accusation,
        "verdict": Verdict,
        "appeal": Appeal
    }

    if not transaction_type in types:
        return jsonify({
        "success": False,
        "message": "Transaction not found"
    }), 404

    t = types[transaction_type].get_random()

    return jsonify({
        "success": True,
        "content": t[transaction_type].to_dict()
    }), 200

# ! This is here for debugging purposes only. It should be soon removed
@app.route('/random_id', methods=['GET'])
def random_id():
    _id = ID.get_random()
    return jsonify({
        "success": True,
        "content": _id["id"].to_dict()
    }), 200

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(
        func=cycle, 
        args=[], 
        trigger='interval', 
        id='job', 
        seconds=30
    )
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)