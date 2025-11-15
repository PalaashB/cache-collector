import sqlite3

DB_PATH = "chatlog.db"

def save_prompt(prompt: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                INSERT OR IGNORE INTO prompts (text)
                VALUES (?);
                """, (prompt,))
    
    conn.commit()
    conn.close()

def save_response(response: str):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        
