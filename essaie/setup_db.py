import mysql.connector

# ⚠️ Modifie ici avec ton mot de passe MySQL
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "ton_mdp"
DB_NAME = "rue_en_folie"

# Connexion au serveur MySQL (sans base)
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Créer la base de données si elle n'existe pas
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
print(f"[INFO] Base {DB_NAME} créée ou déjà existante.")

# Connexion à la base nouvellement créée
conn.database = DB_NAME

# Créer les tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

print("[INFO] Tables 'users' et 'scores' créées ou déjà existantes.")
conn.commit()
cursor.close()
conn.close()
print("[INFO] Base prête pour le jeu !")
