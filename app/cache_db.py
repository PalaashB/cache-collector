import sqlite3

DB_PATH = "./cache.db"


def create_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            prompt TEXT PRIMARY KEY,
            response TEXT
        );
    """)

    conn.commit()
    conn.close()


def get_cached_response(prompt: str):
    """
    Returns the cached response for the given prompt.
    If not found, returns None.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT response FROM cache WHERE prompt = ?;", (prompt,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]
    return None


def save_to_cache(prompt: str, response: str):
    """
    Saves or updates the prompt-response pair in the cache.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO cache (prompt, response)
        VALUES (?, ?);
    """, (prompt, response))

    conn.commit()
    conn.close()



create_table()
