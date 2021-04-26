# Node

The Node is a decentralized sever used to store the user's transactions for a period of time.

### methods
* get_transactions
	* return: the stored transactions
* is_transaction_valid
	* params
		* transaction: a transaction in _dict_ form
		* \_type: the transaction type in _object_ from
	* purpose: to verify if a transaction is valid or not
	* return: a _boolean_ indicatin the transaction's validation
* send_transaction
	* params
		* transaction: a transaction in _dict_ form
		* \_type: the transaction type in _object_ from
	* purpose: to store a transaction if it is valid
	* return: a _boolean_ indicating if the transaction could be added
* connect_nodes
	* params
		* nodes: a _list of dicts_ containing the nodes ip addresses and ports
	* purpose: add to the node's list new nodes
* synchronize
	* purpose: add the transactions from the other nodes that were not added yet
* remove_outdated_transactions
	* purpose: remove any transactions that expired already
