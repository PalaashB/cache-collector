import sqlite3
from sentence_transformers import SentenceTransformer
import numpy as np


DB_PATH = "./data/cache.db"
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            prompt TEXT PRIMARY KEY,
            response TEXT,
            vect BLOB
        );
    """)

    conn.commit()
    conn.close()


def get_cached_response(prompt: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT response FROM cache WHERE prompt = ?;", (prompt,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]
    return None


def save_to_cache(prompt: str, response: str, vect):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()


    #embedding convert
    vect_to_byte= vect.tobytes()

    cur.execute("""
        INSERT OR REPLACE INTO cache (prompt, response, vect)
        VALUES (?, ?, ?);
    """, (prompt, response, vect_to_byte))

    conn.commit()
    conn.close()



create_table()

