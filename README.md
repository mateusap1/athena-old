# Athena
Athena is a decentralized and voluntary justice system, which main focus is to offer a better solution to conflicts that may occur inside a community. The target audience is any group of people who agreed to follow a set of rules and want to have a way of moderating possible conflicts.

For inspiration: 

* https://medium.com/kleros/kleros-a-decentralized-justice-protocol-for-the-internet-38d596a6300d
* https://medium.com/the-crowdjury/the-crowdjury-a-crowdsourced-court-system-for-the-collaboration-era-66da002750d8

### How it works
The Athena blockchain works by having a diversity of transaction types that can be used to create contracts, accuse people of breaking them and solving conflicts by sending a verdict, which determines if the accused must send a payment in order to follow the sentence. The way communities will enforce the payment of fines is up to them and Athena does not solve this problem, as it is a justice system and not a police one. 

Additionally, the way the trials will be executed is also responsability of the parts involved to provide the necessary infrastructure (online or physical). Therefore, Athena is a solution to the frequent unfairness that people encounter in a centralized and coercitive justice system, but does not solve police or trial execution problems.

For one to understand how Athena works, it is extremally important that he understands the transaction types. There are four types of transactions: the **contract**, the **accusation**, the **veredict** and the **appeal**. This transactions can be sent by making a "/send_transaction" POST request to any Node, containing the necessary paramaters. One of the most important paramaters that is needed in all forms of transactions is the **ID**. The ID is a dictionary that contains the user's username (any string with a maximum of 64 characters), e-mail, public key, a nonce (an arbitrary number) and a hash, that needs to have at least five leading zeros.

This ID is extremeally important, because it can be used to avoid spam attacks, as well as, give a real word form of identification to the people that may sign a contract together. Nonetheless, the ID information will be publically available, so it is important that the people who decide to create an ID do not expose any private information or personal e-mails.

In these next topics, we will have a closer look at the transaction types and what they are used for.

### The Contract
A contract can be created by sending a transaction of type **contract** and can be signed by any user that agrees with it's rules. When someone signs a contract, he is saying that he agrees with the rules written and that he promisses to follow them and accept the judges veredict. 

In order for a contract to be valid, it must contain the following paramaters: The **sender's ID** (all transactions should have it), the **rules** (a list of strings), the **list of judges** (a list of IDs) and the **signatures** (a list of RSA signatures with their corresponding IDs).

### The Accusation
After having signed a contract, anyone is able to send an **accusation**. In order for someone to send it, he will need to provide his own **ID**, the **accused ID** and the **contract that was broken**. Both the accused and the first judge in the list will be notified (by e-mail). The judge, after hearing both parts and their lawyers (optional), will send a transaction of type **veredict**. How the judge will decide if the accused is guilty or not is up to him and the involved parts.

### The Veredict
If someone send an accusation, a judge will be warned and will be requested to send a **veredict** within 30 days. He will then hear both the accuser and the accused and make his decision. His decision will be official when he send a veredict to the network, which must include **his own ID**, the **accusation he is responding to** (of type *accusation*), **if the accused is guilty** (a boolean) and a **description** explaining his decision (a string). 

If the judge doesn't send the transaction within the 30 days limit, the next judge from the list will be warned. If this repeats, the next from the list will be requested until there are no more judges, which would automatically declare the accused innocent. Therefore, it is very important to make a decent sized list before sending a contract to the network.

A veredict must be stored by the interested parts and can be shown in communities that recognize this system as a proof that someone is either innocent or guilty.

### The Appeal
If someone disagrees with a veredict, he can still send a transaction of type **appeal**, which must include the **sender's ID** and the **veredict he disagrees with**. The two next judges of the list (after the one that condenmed him) would, after hearing both parts, make their own decisions by sending a transaction of type **veredict**. If both decisions are opposed to the one made by the first judge, he won't receive his reward and the veredict is reverted.

### Practice example
Let's suppose, for instance, that Michael, Jim, Pam, Ryan and Dwight want to make a book club. One of them (let's say Dwight) would write a set of rules that all of them will agree with. Suppose the rules are the following:

* Every month a member must lend three books to the club
* Any member can borrow a maximum of three books every month
* Every end of the month, the books must be given back

Additionally he would write a list of judges and their rewards. Suppose they are the following and the reward is 0.001 BTC:

* Angela
* Andy
* Stanly
* Meredith
* Oscar

After creating this contract by sending a transaction to the network, those who agree with it can start sending their IDs as a response to the contract.

So, for instance, if Michael agrees with the rules writen and trust the listed judges, he will send a **Node_Request** of type **Signature** containing his ID. If Michael was the only one to do this, the community would only be formed by him and Dwight. In our example, though, all of them will do the same as Michael, because they trust the judges and agree with the rules, forming a community of five people.

At this moment, each one would need to lend three books to a community safe (as stated by the initial contract). Let's suppose, though, that Jim don't want to follow the rules and decides to lend only two books. If this happens, any member can send a transaction of type accusation with, as paramaters, Jim's ID and the contract that was broken. 

Angela, the first of the judges list, will then call a meeting (not obrigatory, but recommended) and will analyze each part's side. If Angela doesn't send a veredict within 30 days, she will lose her reward and the next judge (Andy) will be called. If the same thing happens, the new judge will be the next in the list (Stanly). This may continue until there are no more judges. In this case, Jim would automatically be declared innocent.

Assuming this doesn't happen and supposing Angela is not honest, she would declare Jim innocent. Dwight could, then, send a new transaction of type appeal and both Andy and Stanly would make their own veredict. In the case of them being honest and competent, they would send a veredict stating that Jim is actually guilty. This means he would be condemned to pay a fine and Angela would not receive her reward. 

What would happen if Jim did not pay is up to Dwight, Michael, Ryan and Pam. In this case, he would probably be expelled, but in bigger communities, like private cities, the defendant could even be arrested or have justice denied in the future depending on the severity and how the community deals with these cases.

### How it is better than the current justice system
The main reasons our current system is not very good is beacuse it is not voluntary, it is mainly corrupted, it is incompetent and the victim does not earn anything after being wronged. Most of these bad aspects come from the fact that our justice system is centralized and that there is no real incentive for judges to make the right decision and not to accept bribery other than their own moral beliefs and the fear of being fired, which most of the times does not materialize. 

Athena solve most of these issues by being a decentralized, immutable and voluntary network. It is decentralized in the sense that there is no central authority that controls Athena or it's nodes. It is immutable in the sense that no one is able to change a contract without altering it's structure, which would invalidate it. It is voluntary in the sense that no one is forced to accept other people's contracts. 

Athena also offers an incentive to judges in order for them to make the right decision: money. Every judge is paid and if it is later proved that he made the wrong decision, he has to give the money he received back. Additionally, the list of judges is created by the people who signed the contract. This means that, ideally, only trusted people would judge anyone's cases.

### Athena components

#### The Accounts
After initializing the program, a JSON file called "account.json" will be created. This file must contain all contract copies, all signatures and accusations received and all veredicts against or in favor of this person.

Each account will have an ID, that contains an username (a string with a maximum of 64 characters), an e-mail, a public key, a nonce, and a hash (with five leading zeros).

It will be with this account that the user will be able to send and receive any transactions. Whenever the account is initialized, the program will make a request to a trusted nodes to see if there's any transaction with his public key as a target. If that is the case, it will warn the user.

#### The Nodes
Each node will have a "temp_transactions.json" file in which every transaction received from the network will be stored. When a user wants to send a transaction, he will make a "/send_transaction" POST request to a Node, that will, if validated, store his transaction for 24 hours.

In order to avoid spam attacks, the same account will only be able to send twenty transactions per hour.

Every *cycle*, the nodes will make a "/synchronize" GET request, that will verify if the other nodes have any additional transactions and, if they are valid, add these transactions to the JSON file. Additionally, the Nodes will delete any transactions older than 24 hours.

