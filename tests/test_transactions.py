import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from config import contract_config, id_config, verdict_config
from utils import create_key, parse_key, import_key, hash_content
from identity import ID
from transaction.Appeal import Appeal
from transaction.Verdict import Verdict
from transaction.Accusation import Accusation
from transaction.Contract import Contract


MIN_JUDGES = contract_config["minimum_judges"]
MAX_JUDGES = contract_config["maximum_judges"]
MIN_RULES = contract_config["minimum_rules"]
MAX_RULES = contract_config["maximum_rules"]
SENDER_CAN_JUDGE = contract_config["allow_sender_to_judge"]

SENTECE_CHAR_LIMIT = verdict_config["sentence_char_limit"]
DESCRIPTION_CHAR_LIMIT = verdict_config["description_char_limit"]

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

    # Invalid random contract
    c = Contract.get_random(valid=False)["contract"]
    assert c.is_valid() == False

    judges = [ID("Agatha Christie", parsed_pubkey) for _ in range(MIN_JUDGES)]
    rules = ["rule" for _ in range(MIN_RULES)]
    expire = datetime.datetime.now() + datetime.timedelta(days=1)

    # Should be valid as well
    c = Contract(key, userid, rules, judges, expire)
    assert c.is_valid() == True

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
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
    c = Contract(key, userid, rules, [judges[0]
                                      for _ in range(MAX_JUDGES)], expire)
    assert c.is_valid() == False

    expired = datetime.datetime.now() - datetime.timedelta(days=1)
    c = Contract(key, userid, rules, judges, expired)
    assert c.is_valid() == False


def test_accusation():

    # Valid random accusation
    a = Accusation.get_random()["accusation"]
    assert a.is_valid() == True

    # Invalid random accusation
    a = Accusation.get_random(valid=False)["accusation"]
    assert a.is_valid() == False

    judges = [ID.get_random()["id"] for _ in range(MIN_JUDGES)]
    rules = ["rule" for _ in range(MIN_RULES)]
    expire = datetime.datetime.now() + datetime.timedelta(days=1)

    contract = Contract(key, userid, rules, judges, expire)
    accused = ID("Murray Rothbard", parsed_pubkey)

    # Should be valid as well
    a = Accusation(key, userid, accused, contract)
    assert a.is_valid() == True

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid sender's ID
    a = Accusation(key, invalid_id, accused, contract)
    assert a.is_valid() == False

    # Invalid accused's ID
    a = Accusation(key, userid, invalid_id, contract)
    assert a.is_valid() == False

    # Unmatching key
    a = Accusation(create_key(), userid, accused, contract)
    assert a.is_valid() == False

    # Invalid contract
    a = Accusation(key, userid, accused,
                   Contract.get_random(valid=False)["contract"])
    assert a.is_valid() == False


def test_verdict():

    # Valid random verdict
    v = Verdict.get_random()["verdict"]
    assert v.is_valid() == True

    # Invalid random verdict
    v = Verdict.get_random(valid=False)["verdict"]
    assert v.is_valid() == False

    judges = [ID.get_random()["id"] for _ in range(MIN_JUDGES)]
    rules = ["rule" for _ in range(MIN_RULES)]
    expire = datetime.datetime.now() + datetime.timedelta(days=1)
    contract = Contract(key, userid, rules, judges, expire)
    accused = ID("Hercule Poirot", parsed_pubkey)

    accusation = Accusation(key, userid, accused, contract)
    sentence = "Must be executed"
    description = "Because I say so"

    # Should be valid as well
    v = Verdict(key, userid, accusation, sentence, description)
    assert v.is_valid() == True

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid sender's ID
    v = Verdict(key, invalid_id, accusation, sentence, description)
    assert v.is_valid() == False

    # Unmatching key
    v = Verdict(create_key(), userid, accusation, sentence, description)
    assert v.is_valid() == False

    # Invalid accusation
    v = Verdict(key, userid, Accusation.get_random(valid=False)["accusation"],
                sentence, description)
    assert v.is_valid() == False

    # No sentence at all
    v = Verdict(key, userid, accusation, "", description)
    assert v.is_valid() == False

    # Sentence with more chars than the allowed
    v = Verdict(key, userid, accusation, "c" * (SENTECE_CHAR_LIMIT+1), description)
    assert v.is_valid() == False

    # Description with more chars than the allowed
    v = Verdict(key, userid, accusation, sentence, "c" * (DESCRIPTION_CHAR_LIMIT+1))
    assert v.is_valid() == False

def test_appeal():

    # Valid random appeal
    a = Appeal.get_random()["appeal"]
    assert a.is_valid() == True

    # Invalid random appeal
    a = Appeal.get_random(valid = False)["appeal"]
    assert a.is_valid() == False

    judges = [ID.get_random()["id"] for _ in range(MIN_JUDGES)]
    rules = ["rule" for _ in range(MIN_RULES)]
    expire = datetime.datetime.now() + datetime.timedelta(days=1)
    contract = Contract(key, userid, rules, judges, expire)
    accused = ID("Hercule Poirot", parsed_pubkey)
    accusation = Accusation(key, userid, accused, contract)
    sentence = "Must be executed"
    description = "Because I say so"

    verdict = Verdict(key, userid, accusation, sentence, description)

    # Valid hardcoded appeal
    a = Appeal(key, userid, verdict)
    assert a.is_valid() == True

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid sender's ID
    a = Appeal(key, invalid_id, verdict)
    assert a.is_valid() == False
    
    # Unmatching key
    a = Appeal(create_key(), userid, verdict)
    assert a.is_valid() == False

    invalid_verdict = Verdict(key, userid, accusation, "", description)

    # Invalid verdict
    a = Appeal(key, userid, invalid_verdict)
    assert a.is_valid() == False