import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from transaction.Contract import Contract
from identity import ID
from utils import create_key, parse_key, import_key, hash_content
from config import contract_config, id_config


MIN_JUDGES = contract_config["minimum_judges"]
MAX_JUDGES = contract_config["maximum_judges"]
MIN_RULES = contract_config["minimum_rules"]
MAX_RULES = contract_config["maximum_rules"]
SENDER_CAN_JUDGE = contract_config["allow_sender_to_judge"]

HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]


valid_id = ID.get_random()
userid = valid_id["id"]
key = import_key(valid_id["private_key"])
public_key = key.publickey()
parsed_pubkey = parse_key(public_key)


def test_contract():

    # Valid random contract
    c = Contract.get_random()["contract"]
    assert c.is_valid() == True

    judges = [ID.get_random()["id"] for _ in range(MIN_JUDGES)]
    rules = ["rule" for _ in range(MIN_RULES)]
    expire = datetime.datetime.now() + datetime.timedelta(days=1)

    # Should be valid as well
    c = Contract(key, userid, rules, judges, expire)
    assert c.is_valid() == True

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    invalid_id = ID(**content)

    # Invalid ID
    c = Contract(key, invalid_id, rules, judges, expire)
    assert c.is_valid() == False

    # Unmatching key
    c = Contract(create_key(), userid, rules, judges, expire)
    assert c.is_valid() == False

    # No judges
    c = Contract(key, userid, rules, [], expire)
    assert c.is_valid() == False

    # No rules
    c = Contract(key, userid, [], judges, expire)
    assert c.is_valid() == False

    # Sender as judge
    c = Contract(key, userid, rules, [userid], expire)
    assert c.is_valid() == SENDER_CAN_JUDGE

    # Repeated judges
    c = Contract(key, userid, rules, [judges[0] for _ in range(MAX_JUDGES)], expire)
    assert c.is_valid() == False

    expired = datetime.datetime.now() - datetime.timedelta(days=1)
    c = Contract(key, userid, rules, judges, expired)
    assert c.is_valid() == False