from dataclasses import dataclass
from auth import hash_password, is_correct_password

# Ram saving for debug
test_users = {}
DATABASE = "users.db"

@dataclass
class User:
    username: str
    password: str

    fornavn: str
    etternavn: str

    def __post_init__(self):
        self.password = hash_password(self.password, self.username)

    def check_password(self, password: str) -> bool:
        return is_correct_password(password, self.username, self.password)

    @property
    def fullt_navn(self) -> str:
        return f"{self.fornavn} {self.etternavn}"
    

def register_user(user: User, debug: bool = False) -> None:
    if debug:
        test_users[test_users.username.lower()] = user

def login():
    pass

