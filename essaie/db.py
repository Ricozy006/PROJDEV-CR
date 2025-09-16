import sqlite3
import hashlib
import os
import binascii

DB_NAME = "game.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Table scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# -------- Gestion mots de passe --------
def hash_password(password):
    """Retourne 'salt$hash' (PBKDF2-SHA256)."""
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return binascii.hexlify(salt).decode() + "$" + binascii.hexlify(hash_bytes).decode()

def verify_password(password, stored_value):
    """Vérifie mot de passe avec salt+hash stocké."""
    try:
        salt_hex, hash_hex = stored_value.split("$")
        salt = binascii.unhexlify(salt_hex)
        stored_hash = binascii.unhexlify(hash_hex)
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return test_hash == stored_hash
    except Exception:
        return False


# -------- Utilisateurs --------
def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return None  # username déjà pris
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        user_id, stored_pw = result
        if verify_password(password, stored_pw):
            return user_id
    return None


# -------- Scores --------
def save_score(user_id, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (user_id, score))
    conn.commit()
    conn.close()

def get_highscores(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.username, scores.score
    FROM scores
    JOIN users ON scores.user_id = users.id
    ORDER BY scores.score DESC LIMIT ?
    """, (limit,))
    highscores = cursor.fetchall()
    conn.close()
    return highscores