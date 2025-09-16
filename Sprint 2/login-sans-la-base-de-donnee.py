from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Login")
root.resizable(False, False)

width = 300
height = 150

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - width) // 2
y = (screen_height - height) // 5

root.geometry(f"{width}x{height}+{x}+{y}")

def login():
    messagebox.showinfo("Connexion", "Bonjour ! Vous avez bien été connecté.")

def register():
    messagebox.showinfo("Inscription", "Bienvenue ! Votre inscription a été réussie avec succès.")

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
frame_buttons.pack(pady=15)

button_register = Button(frame_buttons, text="S'inscrire", width=15, command=register)
button_register.pack(side=LEFT, padx=10, syy=15)

button_login = Button(frame_buttons, text="Se connecter", width=15, command=login)
button_login.pack(side=LEFT, padx=10)

root.mainloop()
