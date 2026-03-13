from dataclasses import dataclass
import sqlite3

DATABASE = "quotes.db"

@dataclass
class quote:
    content: str
    user: str

    def __post_init__(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO quotes (content, user) VALUES (:content, :user)", self.__dict__)

        conn.commit()
        conn.close()

def get_quote_list() -> list:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    result = cursor.execute("SELECT * FROM quotes").fetchall()

    conn.commit()
    conn.close()

    return result

def delete_quote(id: int) -> None:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM quotes WHERE id = ?", (id, ))

    conn.commit()
    conn.close()

def db_init() -> None:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY,
        content TEXT,
        user TEXT
    )""")

    conn.commit()
    conn.close()

db_init()