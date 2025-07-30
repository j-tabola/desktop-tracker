import tkinter as tk
import webbrowser
from links_manager import get_links, add_link, delete_link
import json
from datetime import datetime, timedelta
import os


class DashboardApp:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.links = []

        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Add Social Link").pack()

        tk.Label(self.frame, text="Website Name:").pack(pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.name_var, width=30).pack(padx=10)

        tk.Label(self.frame, text="Website URL:").pack(pady=5)
        self.url_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.url_var, width=30).pack(padx=10)

        tk.Button(self.frame, text="Add", command=self.add_link).pack(pady=10)

        tk.Button(self.frame, text="Logout", command=self.logout).pack(pady=5)

        self.message = tk.Label(self.frame, text="", fg="red")
        self.message.pack(pady=5)

        self.links_frame = tk.Frame(self.frame)
        self.links_frame.pack()

        self.checkbox_var = tk.BooleanVar()

        tk.Checkbutton(
            self.frame,
            text="Daily Task Complete",
            variable=self.checkbox_var,
            command=self.toggle_all_checkboxes
        ).pack(pady=10)

        self.reset_timer_label = tk.Label(self.frame, text="")
        self.reset_timer_label.pack(pady=5)

        self.update_reset_timer()

        self.load_links()

    def reset_checkboxes(self):
        file_path = self.get_checkbox_file_path()
        today = datetime.now().strftime("%Y-%m-%d")
        with open(file_path, "w") as f:
            json.dump({"date": today, "states": {}}, f)

        for var in self.check_vars.values():
            var.set(False)

        self.checkbox_var.set(False)

    def load_links(self):
        for widget in self.links_frame.winfo_children():
            widget.destroy()

        links = get_links(self.user_id)
        self.check_vars = {}

        checkbox_states = self.load_all_checkbox_states()

        for link_id, link in links:
            row = tk.Frame(self.links_frame)
            row.pack(pady=3, fill="x")
            tk.Label(row, text=link["name"]+" (" + link["url"] +") ").pack(side="left")

            var = tk.BooleanVar()
            self.check_vars[link_id] = var

            var.set(checkbox_states.get(str(link_id), False))

            cb = tk.Checkbutton(row, variable=var,
                    command=lambda lid=link_id, v=var: [self.save_checkbox_state(lid, v), self.update_global_checkbox()])
            cb.pack(side="left")

            tk.Button(row, text="Open", command=lambda u=link["url"]: webbrowser.open(u)).pack(side="left")
            tk.Button(row, text="Delete", command=lambda k=link_id: self.remove_link(k)).pack(side="left")

        self.update_global_checkbox()

    def add_link(self):
        name = self.name_var.get().strip()
        url = self.url_var.get().strip()
        if name == "" or url == "":
            self.message.config(text="Please enter both name and URL", fg="red")
            return
        
        add_link(self.user_id, self.name_var.get(), self.url_var.get())
        self.name_var.set("")
        self.url_var.set("")
        self.load_links()

    def remove_link(self, key):
        delete_link(self.user_id, key)
        self.remove_checkbox_state(key)
        self.load_links()
    
    def logout(self):
        token_path = "token.json"
        if os.path.exists(token_path):
            os.remove(token_path)
        self.frame.destroy()
        from auth import AuthApp
        AuthApp(self.master)

    def get_checkbox_file_path(self):
        return f"daily_check_{self.user_id}.json"

    def update_reset_timer(self):
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        file_path = self.get_checkbox_file_path()

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)

            if data.get("date") != today_str:
                self.reset_checkboxes()

        tomorrow = now.date() + timedelta(days=1)
        midnight = datetime.combine(tomorrow, datetime.min.time())
        remaining = midnight - now

        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.reset_timer_label.config(
            text=f"Resets in {hours:02d}:{minutes:02d}:{seconds:02d}"
        )

        self.frame.after(1000, self.update_reset_timer)

    def load_all_checkbox_states(self):
        file_path = self.get_checkbox_file_path()
        today = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r") as f:
            data = json.load(f)

        if data.get("date") != today:
            self.reset_checkboxes()
            return {}

        valid_link_ids = set(str(link_id) for link_id, _ in get_links(self.user_id))
        current_states = data.get("states", {})
        cleaned_states = {k: v for k, v in current_states.items() if k in valid_link_ids}

        if cleaned_states != current_states:
            
            data["states"] = cleaned_states
            with open(file_path, "w") as f:
                json.dump(data, f)

        return cleaned_states

    def save_checkbox_state(self, link_id, var):
        file_path = self.get_checkbox_file_path()
        today = datetime.now().strftime("%Y-%m-%d")

        data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)

        if data.get("date") != today:
            data = {"date": today, "states": {}}

        if "states" not in data:
            data["states"] = {}

        data["states"][str(link_id)] = var.get()

        with open(file_path, "w") as f:
            json.dump(data, f)

    def update_global_checkbox(self):
        if self.check_vars and all(var.get() for var in self.check_vars.values()):
            self.checkbox_var.set(True)
        else:
            self.checkbox_var.set(False)
    
    def toggle_all_checkboxes(self):
        new_state = self.checkbox_var.get()
        for link_id, var in self.check_vars.items():
            var.set(new_state)
            self.save_checkbox_state(link_id, var)

    def remove_checkbox_state(self, link_id):
        file_path = self.get_checkbox_file_path()

        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        if "states" in data and str(link_id) in data["states"]:
            del data["states"][str(link_id)]

            with open(file_path, "w") as f:
                json.dump(data, f)
