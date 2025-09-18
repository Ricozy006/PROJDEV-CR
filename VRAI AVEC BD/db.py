import mysql.connector
import hashlib
import os
import binascii

# ---------- Database Configuration ----------
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",           # change to your MySQL username
    "password": "Pa$$w0rd",   # change to your MySQL password
    "database": "crossyroad"
}

INIT_CONFIG = DB_CONFIG.copy()
INIT_CONFIG.pop("database")

DB_NAME = "crossyroad"

# ---------- Database Initialization ----------
def initialize_database():
    try:
        print("✅ Connecting to MySQL...")
        conn = mysql.connector.connect(**INIT_CONFIG)
        cursor = conn.cursor()

        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"✅ Database '{DB_NAME}' created or already exists.")

        # Select the database
        cursor.execute(f"USE {DB_NAME};")

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """)
        print("✅ Table 'users' created or already exists.")

        # Create scores table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            score INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        print("✅ Table 'scores' created or already exists.")

        conn.commit()
        print("✅ Initialization complete.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------- Password Utilities ----------
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return binascii.hexlify(salt).decode() + "$" + binascii.hexlify(hash_bytes).decode()

def verify_password(password: str, stored: str) -> bool:
    salt_hex, hash_hex = stored.split("$")
    salt = binascii.unhexlify(salt_hex)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return binascii.hexlify(hash_bytes).decode() == hash_hex

# ---------- User Functions ----------
def create_user(username, password):
    hashed = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        print(f"✅ User '{username}' created.")
        return cursor.lastrowid
    except mysql.connector.IntegrityError:
        print(f"❌ Username '{username}' already exists.")
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
        print(f"✅ Login successful for user '{username}'.")
        return row[0]
    print(f"❌ Login failed for user '{username}'.")
    return None

# ---------- Score Functions ----------
def save_score(user_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (user_id, score) VALUES (%s, %s)", (user_id, score))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Score {score} saved for user ID {user_id}.")

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
    print("🏆 Highscores:")
    for i, (username, score) in enumerate(results, 1):
        print(f"{i}. {username}: {score}")
    return results

# ---------- Main ----------
if __name__ == "__main__":
    initialize_database()

    # Example usage (optional):
    # user_id = create_user("testuser", "testpass")
    # logged_in_id = login("testuser", "testpass")
    # if logged_in_id:
    #     save_score(logged_in_id, 123)
    #     get_highscores()
