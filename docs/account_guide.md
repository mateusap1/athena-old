# Account

The account is what makes it possible to send and receive valid transactions. When an account is first initialized, a private and public key is generated, as well as an ID, which is simply a dictionary containing the user's name, e-mail, public key, nonce and hash. This information is then stored in a newly created JSON file called "account.json".

Most of the following methods were copied from this repository: https://github.com/adi2381/py-blockchain

For a cryptographic basic understanding, this video may be helpful: https://www.youtube.com/watch?v=bRBJ_0I919E&list=PL6TbWIxWsLY3XuAZB4C0_GxrR76TAZOf2

### methods
* create_keys
    * purpose: generates a new pair of private and public key and saves them in the user's harddrive

* create_id
    * purpose: creates an ID based on the user information

* connect_node
    * purpose: assigns the user's node
