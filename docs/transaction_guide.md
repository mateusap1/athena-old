# Transactions

The transactions are what make Athena a justice system and not just a meaningless piece of technology. There are six types of transactions: 
* [Contract](#contract)
* [Accusation](#accusation)
* [Verdict](#verdict)
* [Appeal](#appeal)

## Contract

The **Contract** is a set of rules that any person can agree to follow by sending a signature to the network.

* params
	* privkey: the sender's private key in an **RSAKey** format 
	* sender: the sender's **ID**
	* rules: the rules of the contract in a **list of strings** format
	* judges: the **list of IDs** from the people that will mediate conflicts
	* expire: the **date** (UTC timezone) in which the contract will have no more value

* methods
	* is_valid
		* purpose: to verify if a contract is valid or not
		* return: *bool*
	* to_dict
		* purpose: to join all the contract information, including the hash, in a dictionary form
		* return: *dict*
	* get_content
		* purpose: to join all the essential information of the contract in a dictionary form
		* return: *dict*
	* sign
		* purpose: to store the user's signature
		* return: *None*
	* get_random (static_method)
		* purpose: to generate a random and valid contract
		* params
			* valid: if the generated contract is valid or not (in **bool** format)
		* return: *Contract*

## Accusation

Any member of a given community can send an **Accusation**, which is simply stating that the first judge in the list must send a veredict within 30 days.

* params
	* privkey: the sender's private key in an **RSAKey** format
	* sender: the sender's **ID**
	* accused: the accused's **ID**
	* contract: the broken **contract**

* methods
	* is_valid
		* purpose: to verify if an accusation is valid or not
		* return: *bool*
	* to_dict
		* purpose: to join all the accusation information, including the hash, in a dictionary form
		* return: *dict*
	* get_content
		* purpose: to join only the essential information of the accusation in a dictionary form
		* return: *dict*
	* sign
		* purpose: to store the user's signature
		* return: *None*
	* get_random (static_method)
		* purpose: to generate a random and valid accusation
		* params
			* valid: if the generated contract is valid or not (in **bool** format)
		* return: *Accusation*

## Verdict

After having carefully analyzed the case, the judge must send a transaction of type **Verdict** to the network expressing their opinion about the case, as well as, the sentence, if any, the accused should face.

If the judge don't send a **Veredict** within 30 days, he loses his reward and the next judge in the list will be notified in order to send his own **Verdict** within 30 days.

* params
	* privkey: the sender's private key in an **RSAKey** format
	* sender: the sender's **ID**
	* accusation: the **Accusation** he is analyzing
	* sentence: the punishment in a **str** format (None, if he's not guilty)
	* description: the reason behind his decision in a **str** format

* methods
	* is_valid
		* purpose: to verify if a verdict is valid or not
		* return: *bool*
	* to_dict
		* purpose: to join all the verdict information, including the hash, in a dictionary form
		* return: *dict*
	* get_content
		* purpose: to join only the essential information of the verdict in a dictionary form
		* return: *dict*
	* get_random (static_method)
		* purpose: to generate a random and valid verdict
		* params
			* valid: if the generated contract is valid or not (in **bool** format)
		* return: *Verdict*

## Appeal

If, after a *Verdict*, a user disagreed with the judges decision, he would send a transaction of type **Appeal**, where the two next judges would either make a new decision or keep the previous one. In the case of the sentence being reversed, the first judge would not receive any reward.

* params
	* privkey: the sender's private key in an **RSAKey** format
	* sender: the sender's **ID**
	* verdict: the **Verdict** that is being contested

* methods
	* is_valid
		* purpose: to verify if an appeal is valid or not
		* return: *bool*
	* to_dict
		* purpose: to join all the appeal information, including the hash, in a dictionary form
		* return: *dict*
	* get_content
		* purpose: to join only the essential information of the appeal in a dictionary form
		* return: *dict*
	* get_random (static_method)
		* purpose: to generate a random and valid appeal
		* params
			* valid: if the generated contract is valid or not (in **bool** format)
		* return: *Verdict*
            
