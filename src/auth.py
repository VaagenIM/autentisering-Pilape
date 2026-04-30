import hashlib
import os

pepper = os.environ["PEPPER"] if "PEPPER" in os.environ else 123

def hash_password(key: str, salt: str) -> str:
    passphrase = f"{salt}{key}{pepper}"
    return hashlib.sha512(passphrase.encode('utf-8')).hexdigest()

def is_correct_password(key: str, salt: str, hashed_password: str) -> bool:
    return hash_password(key, salt) == hashed_password
