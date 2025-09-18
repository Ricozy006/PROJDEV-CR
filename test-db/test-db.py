# Projet : Base de donnée
# Auteur : Luca Giubbilei
# date : 13.03.2024
# Source d'aide : Alexandre Tercier

from tkinter import *
from tkinter import messagebox
import sqlite3
import os
username1 = ""

root = Tk()
root.title("Login")

width = 300
height = 150

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#chagpt nous a un peu aidé pour réaliser cette petite partit
x = (screen_width - width) // 2
y = (screen_height - height) // 5

root.geometry(f"{width}x{height}+{x}+{y}")




def create_database():
    conn = sqlite3.connect('login_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tusers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            top_score INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def register():
    global username1
    username = entry_username.get()
    password = entry_password.get()
    username1 = username
    if username and password:
        conn = sqlite3.connect('login_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tusers WHERE username=?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Erreur", "Le nom d'utilisateur est déjà pris veuillez en prendre un autre.")
        else:
            cursor.execute('INSERT INTO tusers (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Inscription", "Bienvenue ! Votre inscription a été réussie avec succès.")
    else:
        messagebox.showerror("Erreur", "Veuillez rentrer un nom d'utilisateur et un mot de passe.")

#fonction pour ouvrir le jeux une fois le login bien éffectuer

def open_game():
    global username1
    os.system(f"python 2048_game_1.py {username1}")


def login():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        conn = sqlite3.connect('login_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tusers WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Connexion réussie", "Bienvenue, {}!".format(username))
            root.destroy()
            open_game()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        messagebox.showerror("Erreur", "Le nom d'utilisateur et le mot de passe sont requis.")



# Creation de la base de données
create_database()


# Frame principale avec padding
frame_main = Frame(root, padx=20, pady=20)
frame_main.pack(fill="both", expand=True)

# Frame pour username
frame_user = Frame(frame_main)
frame_user.pack(fill="x", pady=5)

label_user = Label(frame_user, text="Username :", font=("Helvetica", 11), width=10, anchor='w')
label_user.pack(side=LEFT)

entry_username = Entry(frame_user, font=("Helvetica", 11))
entry_username.pack(side=LEFT, fill="x", expand=True)
entry_username.focus()

# Frame pour password
frame_password = Frame(frame_main)
frame_password.pack(fill="x", pady=5)

label_password = Label(frame_password, text="Password :", font=("Helvetica", 11), width=10, anchor='w')
label_password.pack(side=LEFT)

entry_password = Entry(frame_password, show="*", font=("Helvetica", 11))
entry_password.pack(side=LEFT, fill="x", expand=True)

# Frame pour les boutons
frame_buttons = Frame(frame_main)
frame_buttons.pack(pady=5)

#Bouttons
button_register = Button(frame_buttons, text="S'inscrire", width=15, command=register)
button_register.pack(side=LEFT, padx=10, pady=5)

button_login = Button(frame_buttons, text="Se connecter", width=15, command=login)
button_login.pack(side=LEFT, padx=10, pady=3)





root.mainloop()