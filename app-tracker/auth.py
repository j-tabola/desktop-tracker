import tkinter as tk
import re
from firebase_config import auth
from dashboard import DashboardApp
from auth_helpers import create_user_document, create_cache_login, load_cached_login
import os

class AuthApp:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        self.email = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self.frame, text="Email").pack(anchor="w")
        tk.Entry(self.frame, textvariable=self.email).pack(fill="x")
        tk.Label(self.frame, text="Password").pack(anchor="w")
        tk.Entry(self.frame, show="*", textvariable=self.password).pack(fill="x")

        self.message = tk.Label(self.frame, text="", fg="red")
        self.message.pack(pady=5)

        tk.Button(self.frame, text="Login", command=self.login).pack(side="left", padx=5, pady=10)
        tk.Button(self.frame, text="Sign Up", command=self.signup).pack(side="left", padx=5, pady=10)

        cached = load_cached_login()
        if cached:
            email, password = cached
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                create_user_document(user['localId'], email)
                self.frame.destroy()
                DashboardApp(self.master, user['localId'])
            except:
                pass

    def validate_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    def login(self):
        email = self.email.get().strip()
        password = self.password.get()
        if not email or not password:
            self.message.config(text="Please enter email and password", fg="red")
            return

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            create_user_document(user['localId'], email)
            self.message.config(text="Login successful!", fg="green")

            if not os.path.exists("token.json"):
                create_cache_login(email, password)

            self.frame.destroy()
            DashboardApp(self.master, user['localId'])
        except:
            self.message.config(text=f"Login failed: check credentials", fg="red")

    def signup(self):
        email = self.email.get().strip()
        password = self.password.get()

        if not self.validate_email(email):
            self.message.config(text="Invalid email format", fg="red")
            return

        if len(password) < 6:
            self.message.config(text="Password must be at least 6 characters", fg="red")
            return

        try:
            user = auth.create_user_with_email_and_password(email, password)
            create_user_document(user['localId'], email)

            self.message.config(text="Signup successful!", fg="green")
        except:
            self.message.config(text=f"Signup failed, Try again.", fg="red")
