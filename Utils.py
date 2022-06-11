import hashlib


def hash_str(input_str: str) -> str:
    hashed_str = hashlib.md5(input_str.encode("utf8")).hexdigest()
    return hashed_str
