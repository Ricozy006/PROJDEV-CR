import mysql.connector
import hashlib
import os
import binascii

# ⚠️ Modifie ici avec ton mot de passe MySQL
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "ton_mdp",
    "database": "rue_en_folie"
}

# Connexion
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Hash mot de passe
def hash_password(password):
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return binascii.hexlify(salt).decode() + "$" + binascii.hexlify(hash_bytes).decode()

def verify_password(password, stored_value):
    try:
        salt_hex, hash_hex = stored_value.split("$")
        salt = binascii.unhexlify(salt_hex)
        stored_hash = binascii.unhexlify(hash_hex)
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return test_hash == stored_hash
    except Exception:
        return False

# Créer un utilisateur
def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        user_id = cursor.lastrowid
    except mysql.connector.IntegrityError:
        user_id = None  # Username déjà pris
    conn.close()
    return user_id

# Login
def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        user_id, stored_pw = result
        if verify_password(password, stored_pw):
            return user_id
    return None

# Sauvegarder score
def save_score(user_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (user_id, score) VALUES (%s, %s)", (user_id, score))
    conn.commit()
    conn.close()

# Récupérer les meilleurs scores
def get_highscores(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, scores.score
        FROM scores
        JOIN users ON scores.user_id = users.id
        ORDER BY scores.score DESC
        LIMIT %s
    """, (limit,))
    highscores = cursor.fetchall()
    conn.close()
    return highscores
