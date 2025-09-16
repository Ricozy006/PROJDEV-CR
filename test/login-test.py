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
root.resizable(False, False)
root.geometry("250x100")

#
# def register():
#     global username1
#     username = entry_username.get()
#     password = entry_password.get()
#     username1 = username
#     if username and password:
#         conn = sqlite3.connect('login_db.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM tusers WHERE username=?', (username,))
#         existing_user = cursor.fetchone()
#         if existing_user:
#             messagebox.showerror("Erreur", "Le nom d'utilisateur est déjà pris veuillez en prendre un autre.")
#         else:
#             cursor.execute('INSERT INTO tusers (username, password) VALUES (?, ?)', (username, password))
#             conn.commit()
#             conn.close()
#             messagebox.showinfo("Inscription", "Bienvenue ! Votre inscription a été réussie avec succès.")
#     else:
#         messagebox.showerror("Erreur", "Veuillez rentrer un nom d'utilisateur et un mot de passe.")
#
#
# def open_game():
#     global username1
#     os.system(f"python 2048_game_1.py {username1}")
#
#
# def login():
#     username = entry_username.get()
#     password = entry_password.get()
#     if username and password:
#         conn = sqlite3.connect('login_db.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM tusers WHERE username=? AND password=?', (username, password))
#         user = cursor.fetchone()
#         if user:
#             messagebox.showinfo("Connexion réussie", "Bienvenue, {}!".format(username))
#             root.destroy()
#             open_game()
#         else:
#             messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
#     else:
#         messagebox.showerror("Erreur", "Le nom d'utilisateur et le mot de passe sont requis.")



#frame
frame_user = Frame(root)
frame_user.pack(fill="x", anchor=N)

frame_password = Frame(root)
frame_password.pack(fill="x", anchor=N)

frame_boutton = Frame(root)
frame_boutton.pack(fill="x", anchor=N)

#Label
label_user = Label(frame_user, text="Username :", font=("Helvetica", 10))
label_user.pack(padx=3, side=LEFT)

label_password = Label(frame_password, text="Password :", font=("Helvetica", 10))
label_password.pack(padx=3, side=LEFT)


#Entry
entry_username = Entry(frame_user)
entry_username.pack(padx=5,side=LEFT)
entry_username.focus()

entry_password = Entry(frame_password, show="*")
entry_password.pack(padx=6, side=LEFT)


#Boutton
button_register = Button(frame_boutton, text="S'inscrire")
button_register.pack(pady=10, side=LEFT, padx=6)

button_login = Button(frame_boutton, text="Se connecter")
button_login.pack(pady=10, side=RIGHT, padx=6)



root.mainloop()

