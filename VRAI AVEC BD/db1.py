import mysql.connector

INIT_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",           # change par ton user
    "password": "Pa$$w0rd"     # change par ton mdp
}

DB_NAME = "crossyroad"

def initialize_database():
    try:
        print("✅ Connexion à MySQL...")
        conn = mysql.connector.connect(**INIT_CONFIG)
        cursor = conn.cursor()

        # Créer la base si elle n'existe pas
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"✅ Base '{DB_NAME}' créée ou existante.")

        # Sélectionner la base
        cursor.execute(f"USE {DB_NAME};")

        # Créer table users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """)
        print("✅ Table 'users' créée ou existante.")

        # Créer table scores
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            score INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        print("✅ Table 'scores' créée ou existante.")

        conn.commit()
        print("✅ Initialisation terminée.")

    except mysql.connector.Error as err:
        print(f"❌ Erreur MySQL : {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()
