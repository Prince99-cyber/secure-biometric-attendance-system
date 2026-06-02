import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import os

ADMIN_PASSWORD = "1234"

root = tk.Tk()

root.title("Biometric Attendance System")

root.geometry("800x500")

root.configure(bg="#0f172a")

title = tk.Label(
    root,
    text="BIOMETRIC ATTENDANCE SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#0f172a",
    fg="cyan"
)

title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Face Recognition Attendance & Authentication",
    font=("Arial", 14),
    bg="#0f172a",
    fg="white"
)

subtitle.pack(pady=5)

time_label = tk.Label(
    root,
    font=("Arial", 16, "bold"),
    bg="#0f172a",
    fg="lightgreen"
)

time_label.pack(pady=15)

def update_time():

    current_time = datetime.now().strftime("%d-%m-%Y   %H:%M:%S")

    time_label.config(text=current_time)

    root.after(1000, update_time)

update_time()

status_label = tk.Label(
    root,
    text="System Ready",
    font=("Arial", 14),
    bg="#0f172a",
    fg="yellow"
)

status_label.pack(pady=10)

button_frame = tk.Frame(root, bg="#0f172a")

button_frame.pack(pady=20)

def register_face():

    user_id = simpledialog.askstring(
        "Register User",
        "Enter faculty id:"
    )

    if user_id:

        os.system(f'python start.py "{user_id}"')

def train_model():

    os.system("python start.py test")

def admin_setup():

    password = simpledialog.askstring(
        "Admin Login",
        "Enter Admin Password:",
        show="*"
    )

    if password == ADMIN_PASSWORD:

        admin_window = tk.Toplevel(root)

        admin_window.title("Admin Panel")

        admin_window.geometry("400x300")

        admin_window.configure(bg="#1e293b")

        tk.Label(
            admin_window,
            text="ADMIN PANEL",
            font=("Arial", 20, "bold"),
            bg="#1e293b",
            fg="cyan"
        ).pack(pady=20)

        tk.Button(
            admin_window,
            text="Register Face",
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
            bg="cyan",
            fg="black",
            command=register_face
        ).pack(pady=15)

        tk.Button(
            admin_window,
            text="Train Model",
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
            bg="lightgreen",
            fg="black",
            command=train_model
        ).pack(pady=15)

    else:

        messagebox.showerror("Error", "Wrong Password")

def login():

    status_label.config(text="Scanning Face...")

    os.system("python recognize.py")

    status_label.config(text="Scan Completed")

login_button = tk.Button(
    button_frame,
    text="FACE LOGIN",
    width=20,
    height=2,
    font=("Arial", 14, "bold"),
    bg="cyan",
    fg="black",
    relief="raised",
    command=login
)

login_button.grid(row=0, column=0, padx=20, pady=10)

admin_button = tk.Button(
    button_frame,
    text="ADMIN SETUP",
    width=20,
    height=2,
    font=("Arial", 14, "bold"),
    bg="orange",
    fg="black",
    relief="raised",
    command=admin_setup
)

admin_button.grid(row=0, column=1, padx=20, pady=10)

exit_button = tk.Button(
    root,
    text="EXIT",
    width=15,
    height=2,
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    command=root.quit
)

exit_button.pack(pady=20)

footer = tk.Label(
    root,
    text="Developed by team x",
    font=("Arial", 10),
    bg="#0f172a",
    fg="gray"
)

footer.pack(side="bottom", pady=10)

root.mainloop()