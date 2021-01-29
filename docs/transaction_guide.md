## Transactions

The transactions are what make Athena a justice system and not just a meaningless piece of technology. There are six types of transactions: 
* [Payment](#payment)
* [Contract](#contract)
* [Recon](#recon)
* [Accusation](#accusation)
* [Defense](#defense)
* [Veredict](#veredict)

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
            * Returns everything except the signature and the hash on a dictionary format

* ## Contract

    The contract is basically a set of rules that any person can agree to follow, accepting to be responsible for any rules that he may break in exchange of making part of a community. 

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * rules: the rules of the contract on a list format

    * ### methods
        * ### to_dict
            * Returns all the contract content on a dictionary format
        
        * ### get_content
            * Returns everything except the signature and the hash on a dictionary format

* ## Recon

    In order for you to sign a contract, you simply need to send a **Recon** transaction. 

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * receiver: the public key of the person you want to form a *community* with
        * contract: the contract you both want to sign

    * ### methods
        * ### to_dict
            * Returns all the contract content on a dictionary format
        
        * ### get_content
            * Returns everything except the signature and the hash on a dictionary format

* ## Accusation

    Any member of a given community can send an accusation transaction by specifying the accused, the contract, the rule he broke and the judge he chooses to the case

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * accused: the public key of the accused in a string format
        * contract: the contract that the accused supposedly broke
        * rule_index: the index of the rule the accused may have broken
        * proposed_fine: the amount that should be paid to the victim according to the accusator
        * judge: any member from this community that the sender thinks would be a good arbitrator

    * ### methods
        * ### to_dict
            * Returns all the contract content on a dictionary format

        * ### get_content
            * Returns everything except the signature and the hash on a dictionary format

* ## Defense

    After being accused by someone of breaking a rule, the user can send a transaction of type *Defense*, choosing a member he thinks will be a good jugde

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * accusation: the accusation transaction that was sent against him
        * judge: any member from this community that the sender thinks would be a good arbitrator

    * ### methods
        * ### to_dict
            * Returns all the contract content on a dictionary format

        * ### get_content
            * Returns everything except the signature and the hash on a dictionary format

* ## Veredict

    After having carefully analyzed the case, each judge and member of the jury should send a transaction of type veredict to the blockchain expressing their opinion on the case, as well as, if they think the accused is guilty (and the fine is reasonable). If they think that the accusated is guilty but the fine is absurd, they should mark as if the accusated is not guilty, to the accusator opens a new transaction with a reasonable value.

    * ### params
        * sender: the public key of the sender in a string format
        * fee: the amount that will be paid to the miners in a float format
        * accusation: the accusation transaction that was sent against him
        * is_guilty: if the accusated is guilty and the proposed fine is reasonable (True or False)
        * description: why they made this veredict

    * ### methods
        * ### to_dict
            * Returns all the contract content on a dictionary format

        * ### get_content
            * Returns everything except the signature and the hash on a dictionary format
            