import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from config import id_config
from utils import create_key, parse_key, hash_content
from identity import ID


HASH_DIFFICULTY = id_config["hash_difficulty"]
NONCE_LIMIT = id_config["nonce_limit"]
USERNAME_LIMIT = id_config["username_char_limit"]


key = create_key()
public_key = key.publickey()
parsed_pubkey = parse_key(public_key)


def test_ids():

    # Verify if the random contract is valid
    assert ID.get_random()["id"].is_valid() == True
    assert ID.is_id_valid(ID.get_random()["id"].to_dict()) == True

    # Verify if the random contract is not valid (when valid == False)
    assert ID.get_random(valid = False)["id"].is_valid() == False
    assert ID.is_id_valid(ID.get_random(valid = False)["id"].to_dict()) == False

    # Should be valid
    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY, NONCE_LIMIT)

    assert ID.is_id_valid(content) == True

    userid = ID(**content)
    assert userid.is_valid() == True

    # Exceeding chars limit
    content = hash_content({
        "username": "a" * (USERNAME_LIMIT + 2),
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY, NONCE_LIMIT)

    assert ID.is_id_valid(content) == False

    userid = ID(**content)
    assert userid.is_valid() == False

    # Tempering the data
    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY, NONCE_LIMIT)

    content["username"] = "Albert Einsten"

    assert ID.is_id_valid(content) == False

    userid = ID(**content)
    assert userid.is_valid() == False

    # Making the hash easier
    content = hash_content({
        "username": "Isaac Newton",
        "public_key": parsed_pubkey
    }, HASH_DIFFICULTY - 1, NONCE_LIMIT)
    content["hash_value"] = content["hash_value"].replace("0", "a")

    assert ID.is_id_valid(content) == False

    userid = ID(**content)
    assert userid.is_valid() == False