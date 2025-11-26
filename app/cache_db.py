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

    # promptvector=embedder.encode(prompt)

    # cur.execute("SELECT response FROM cache WHERE prompt = ?;", (prompt,))
    # row = cur.fetchone()



    # for i in row:
    #     if cosine_sim(i,promtvector) > 0.85: #tweak
    #         return 

    promptvector=embedder.encode(prompt)
    
    cur.execute("SELECT response, vect FROM cache")
    lis= cur.fetchall()

    vectors = []

    responses= []   #creating lists to compare vectors and fetch response

    for response, blob in lis:
        vec = np.frombuffer(blob, dtype=np.float32)  
        vectors.append(vec)
        responses.append(response)



    for i in vectors:
        if cosine_sim(promptvector, i) > 0.85:
            return responses[vectors.index(i)]
            
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

def cosine_sim(vect1, vect2):
    vect1=np.array(vect1)
    vect2=np.array(vect2)

    dot = np.dot(vect1, vect2)
    norm1 = np.linalg.norm(vect1)
    norm2 = np.linalg.norm(vect2)

    if norm1 == 0 or norm2 == 0:
        return 0.0  
    
    sim= dot/(norm1*norm2)

    return sim


create_table()

