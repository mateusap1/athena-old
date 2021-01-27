## Transactions

The transactions are what make Athena a justice system and not just a meaningless piece of technology. There are three types of transactions: The payment, the contract and the judgement.

* ## Payment

    Even though, the first idea was to use bitcoin or monero as a way of paying miners and judges, it became clear with time that this would not be a good solution as it would create the problem of having to pay "double fees" and could also be a security problem as the Athena software would not have direct access to these blockchains. The solution found was to create its own cryptocurrency, not with the intention of competing in the monetary field, but only to create a stymulus to both miners and judges without having to count on third party forms of payment.

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * amount: the amount that is being sent in a float format
        * receiver: the public key of the user that will receive this amount in a string format

    * ### methods
        * ### to_dict
            * Returns all the payment content on a dictionary format
        
        * ### get_content
            * Returns everything except the signature on a dictionary format

* ## Contract

    The contract is basically a set of rules that any person can agree to follow, accepting to be responsible for any rules that he may break in exchange of making part of a community. 

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * rules: the rules of the contract on a list format

    * ### methods
        * ### to_dict
            * Returns all the contract content on a dictionary format
        
        * ### sign_contract
            * Adds to the signatures array this private_keys signature

            * params:
                * private_key: the users private key in a string format
            
        * ### verify_signature
            * Checks if this public_key signed the contract

            * params:
                * public_key: the users public key in a string format
            
            * Returns true if the public key signed it and false otherwise
            