from dataclasses import dataclass
from auth import hash_password, is_correct_password

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
    def fullt_navn(self):
        return f"{self.fornavn} {self.etternavn}"