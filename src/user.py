from dataclasses import dataclass
from auth import hash_password, is_correct_password

import sqlite3
DATABASE = "users.db"

@dataclass
class User:
    username: str
    password: str

    _loaded_from_db: bool = False

    def __post_init__(self):
        if self._loaded_from_db:
            return
        self.username = self.username.lower()
        self.password = hash_password(self.password, self.username)
        self._loaded_from_db = True
        self.register_to_db()

    def check_password(self, password: str) -> bool:
        return is_correct_password(password, self.username, self.password)
    

    def register_to_db(self) -> None:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO users (username, password)
        VALUES (:username, :password)""", self.__dict__)

        conn.commit()
        conn.close()

def get_user(username: str) -> User | None:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    result = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    conn.commit()
    conn.close()

    if result == None:
        return result

    return User(*result, _loaded_from_db=True)

def db_init() -> None:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        UNIQUE(username)
    )""")

    conn.commit()
    conn.close()

db_init()