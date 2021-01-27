## Blockchain

It’s the class that will be used to initialize the blockchain it self. When initializing 	a blockchain object, you are able to do a variaty of actions that will be then saved 	on the specified directory (the path must be specified in “config.py”).

### params
* store_object: if true, stores the blockchain inside the persons hard drive

### methods

* ### create_block
    * Appends a block to the end of the chain with the transactions that are in the transactions list

    * params:
        * proof: the proof of work from the block.
        * previous_hash: the hash of the previous block.

    * Returns the block that was created

* ### get_previous_block
    * Returns the last block of the current chain

* ### get_mining_difficulty
    * Calculates the number of leading zeros that approaches the time goal of mining one block each 120 seconds

    * Returns the mining difficulty

* ### get_current_reward
    * Calculates the ideal reward to the miners

    * Returns the reward value

* ### proof_of_work
    * Calculates the nonce that when hashed with the previous proof gives a number with N leading zeros, where N is the current mining difficulty

    * params:
        * previous_proof: the proof of the previous block.

    * Returns the nonce that was found

* ### proof_of_work
    * Calculates the nonce that when hashed with the previous proof gives a number with N leading zeros, where N is the current mining difficulty

    * params:
        * previous_proof: the proof of the previous block.

    * Returns the nonce that was found

* ### add_transaction
    * Adds a transaction to the blockchain list

    * params:
        * transaction: the transaction that will be appended to the list

    * Returns index of current block

* ### get_balance
    * Calculates the current balance of a given public key

    * params:
        * public_key: the users public key

    * Returns the calculated balance

* ### add_node
    * Adds a node to the list

    * params:
        * address: the node ip address

* ### replace_chain
    * Replaces the current chain with the longest compared to the connected nodes ones (if they are valid)

    * Returns true if the chain was replaced and false otherwise

* ### get_dict_list
    * Returns the blockchain in form of a dictionary

* ### get_dict_list
    * Transforms a json object into a list of blocks
    
    * Returns the transformed list