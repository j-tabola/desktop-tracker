import tkinter as tk
from auth import AuthApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Social Media Dashboard")
    root.geometry("800x600")
    app = AuthApp(root)
    root.mainloop()
