path_files = {
    "node_path": "/home/mateusap1/Documents/athena_core/node",
    "account_path": "/home/mateusap1/Documents/athena_core/account"
}

id_config = {
    "username_char_limit": 64,
    "nonce_limit": 10**6,
    "date_format": "%Y-%m-%d %H:%M:%S.%f",
    "hash_difficulty": 5
}

contract_config = {
    "minimum_judges": 1,
    "maximum_judges": 256,
    "minimum_rules": 1,
    "maximum_rules": 1024,
    "allow_sender_to_judge": False
}

verdict_config = {
    "sentence_char_limit": 4096,
    "description_char_limit": 8192
}

node_config = {
    "transactions_daylimit": 5
}