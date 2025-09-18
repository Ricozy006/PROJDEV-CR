import mysql.connector
import hashlib, os, binascii

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",           # change avec ton user MySQL
    "password": "Pa$$w0rd",    # change avec ton mot de passe
    "database": "crossyroad"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------- Password utils ----------
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return binascii.hexlify(salt).decode() + "$" + binascii.hexlify(hash_bytes).decode()

def verify_password(password: str, stored: str) -> bool:
    salt_hex, hash_hex = stored.split("$")
    salt = binascii.unhexlify(salt_hex)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return binascii.hexlify(hash_bytes).decode() == hash_hex

# ---------- User functions ----------
def create_user(username, password):
    hashed = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.IntegrityError:
        return None
    finally:
        cursor.close()
        conn.close()

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row and verify_password(password, row[1]):
        return row[0]
    return None

# ---------- Score functions ----------
def save_score(user_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (user_id, score) VALUES (%s, %s)", (user_id, score))
    conn.commit()
    cursor.close()
    conn.close()

def get_highscores(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username, s.score
        FROM scores s
        JOIN users u ON s.user_id = u.id
        ORDER BY s.score DESC
        LIMIT %s
    """, (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
