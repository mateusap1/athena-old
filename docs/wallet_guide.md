## Wallet

The wallet is the member identity. It is with the wallet that they are able to make and receive transactions.

Most of the following methods were copied from this repo: https://github.com/adi2381/py-blockchain
For a cryptographic basic understanding, this video may be helpful: https://www.youtube.com/watch?v=bRBJ_0I919E&list=PL6TbWIxWsLY3XuAZB4C0_GxrR76TAZOf2

### methods
* ### generate_keys
    * Generates a new pair of private and public key

    * Returns the generated pair of keys in hexadecimal

* ### create_keys
    * Creates a new pair of public and private keys by using generate_keys static method
    
* ### sign_transaction
    * Creates a signature using the wallet private key and the transaction content and assigns it to the transaction signature variable

    * params:
        * transaction: the transaction that will be signed

* ### verify_transaction
    * Verifies if a transaction signature is valid

    * params:
        * transaction: the transaction that will be signed
    
    * Returns true if the signature was valid and false otherwise

* ### get_balance
    * Gets the current balance of the wallet

    * params:
        * blockchain: the blockchain the wallet is in
    
    * Returns the current balance