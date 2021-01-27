## Block

The block is the most important part of the blockchain. It is in the block that the blockchain transactions can be found. Any user can add a block to the blockchain, but it will only be valid if its transactions are valid and the proof number is valid. A proof number is valid when the hash operation has the required amount of leading zeros, which are specified by a blockchain method.

### params
* index: the position of the block in the chain
* timestamp: The time the block was mined
* transactions: The transactions added to this block
* proof: The number that the miner had to find in order to make this block valid
* previous_hash: The hash of the previous block

### methods
* ### get_hash
    * Calculates a sha256 hash representation of the block dictionary

    * Returns this hashed value in a hexadecimal format

* ### get_dict
    * Returns a dictionary version of the block

* ### dict_to_object
    * Transforms a dictionary into a block object

    * params:
        * dict_version: the dictionary with all the necessary paramaters to make a block object

    * Returns the block object