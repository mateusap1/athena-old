import sys
import os
import datetime
import pytest

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
    c = Contract(userid, rules, judges, expire)
    c.sign(key)
    assert c.is_valid() == True

    # Make sure the class raises an exception when the
    # paramaters aren't from the correct type
    with pytest.raises(TypeError):
        c = Contract("User", rules, judges, expire)
    with pytest.raises(TypeError):
        c = Contract(userid, [1, 2, 3], judges, expire)
    with pytest.raises(TypeError):
        c = Contract(userid, rules, ["Miss Marple"], expire)
    with pytest.raises(TypeError):
        c = Contract(userid, rules, judges, "Tomorrow")

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid ID
    c = Contract(invalid_id, rules, judges, expire)
    c.sign(key)
    assert c.is_valid() == False

    # Unmatching key
    c = Contract(userid, rules, judges, expire)
    c.sign(create_key())
    assert c.is_valid() == False

    # No judges
    c = Contract(userid, rules, [], expire)
    c.sign(key)
    assert c.is_valid() == False

    # No rules
    c = Contract(userid, [], judges, expire)
    c.sign(key)
    assert c.is_valid() == False

    # Sender as judge
    c = Contract(userid, rules, [userid], expire)
    c.sign(key)
    assert c.is_valid() == SENDER_CAN_JUDGE

    # Repeated judges
    c = Contract(userid, rules, [judges[0] for _ in range(MAX_JUDGES)], expire)
    c.sign(key)
    assert c.is_valid() == False

    expired = datetime.datetime.now() - datetime.timedelta(days=1)
    c = Contract(userid, rules, judges, expired)
    c.sign(key)
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

    contract = Contract(userid, rules, judges, expire)
    contract.sign(key)
    accused = ID("Murray Rothbard", parsed_pubkey)

    # Should be valid as well
    a = Accusation(userid, accused, contract)
    a.sign(key)
    assert a.is_valid() == True

    with pytest.raises(TypeError):
        a = Accusation("User", accused, contract)
    with pytest.raises(TypeError):
        a = Accusation(userid, "Accused", contract)
    with pytest.raises(TypeError):
        a = Accusation(userid, accused, {"content": "..."})

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid sender's ID
    a = Accusation(invalid_id, accused, contract)
    a.sign(key)
    assert a.is_valid() == False

    # Invalid accused's ID
    a = Accusation(userid, invalid_id, contract)
    a.sign(key)
    assert a.is_valid() == False

    # Unmatching key
    a = Accusation(userid, accused, contract)
    a.sign(create_key())
    assert a.is_valid() == False

    # Invalid contract
    a = Accusation(userid, accused,
                   Contract.get_random(valid=False)["contract"])
    a.sign(key)
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
    contract = Contract(userid, rules, judges, expire)
    contract.sign(key)
    accused = ID("Hercule Poirot", parsed_pubkey)

    accusation = Accusation(userid, accused, contract)
    accusation.sign(key)
    sentence = "Must be executed"
    description = "Because I say so"

    # Should be valid as well
    v = Verdict(userid, accusation, sentence, description)
    v.sign(key)
    assert v.is_valid() == True

    with pytest.raises(TypeError):
        v = Verdict("User", accusation, sentence, description)
    with pytest.raises(TypeError):
        v = Verdict(userid, {"content": "..."}, sentence, description)
    with pytest.raises(TypeError):
        v = Verdict(userid, accusation, False, description)
    with pytest.raises(TypeError):
        v = Verdict(userid, accusation, sentence, 76)

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid sender's ID
    v = Verdict(invalid_id, accusation, sentence, description)
    v.sign(key)
    assert v.is_valid() == False

    # Unmatching key
    v = Verdict(userid, accusation, sentence, description)
    v.sign(create_key())
    assert v.is_valid() == False

    # Invalid accusation
    v = Verdict(userid, Accusation.get_random(valid=False)["accusation"],
                sentence, description)
    v.sign(key)
    assert v.is_valid() == False

    # No sentence at all
    v = Verdict(userid, accusation, "", description)
    v.sign(key)
    assert v.is_valid() == False

    # Sentence with more chars than the allowed
    v = Verdict(userid, accusation, "c" * (SENTECE_CHAR_LIMIT+1), description)
    v.sign(key)
    assert v.is_valid() == False

    # Description with more chars than the allowed
    v = Verdict(userid, accusation, sentence, "c" * (DESCRIPTION_CHAR_LIMIT+1))
    v.sign(key)
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

    contract = Contract(userid, rules, judges, expire)
    contract.sign(key)

    accused = ID("Hercule Poirot", parsed_pubkey)
    accusation = Accusation(userid, accused, contract)
    accusation.sign(key)

    sentence = "Must be executed"
    description = "Because I say so"

    verdict = Verdict(userid, accusation, sentence, description)
    verdict.sign(key)

    # Valid hardcoded appeal
    a = Appeal(userid, verdict)
    a.sign(key)
    assert a.is_valid() == True

    with pytest.raises(TypeError):
        a = Appeal("User", verdict)
    with pytest.raises(TypeError):
        a = Appeal(userid, {"content": "..."})

    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)

    content["hash_value"] = content["hash_value"].replace("0", "a")
    invalid_id = ID(**content)

    # Invalid sender's ID
    a = Appeal(invalid_id, verdict)
    a.sign(key)
    assert a.is_valid() == False
    
    # Unmatching key
    a = Appeal(userid, verdict)
    a.sign(create_key())
    assert a.is_valid() == False

    invalid_verdict = Verdict(userid, accusation, "", description)
    invalid_verdict.sign(key)

    # Invalid verdict
    a = Appeal(userid, invalid_verdict)
    a.sign(key)
    assert a.is_valid() == False