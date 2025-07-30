# App Tracker

A simple desktop app built with Python and Tkinter to help you manage and track daily completion of links (e.g. social media check-ins, work tools, etc.). Includes Firebase authentication and Firestore integration.

---

## Features

-  Login and account caching using Firebase Authentication  
-  Add, open, and remove custom website links  
-  Daily task checkboxes with reset at midnight  
-  Automatic daily reset of checkbox states  
-  Global "All Complete" checkbox synced with individual link checkboxes  
-  Local state stored per user using JSON  
-  Persistent Firestore storage for links  
-  Token cache and daily checkbox state stored locally  
-  Packaged as a standalone `.exe` using PyInstaller  

---

## Project structure
```plaintext
app-tracker/
│
├── main.py
├── auth.py
├── dashboard.py
├── links_manager.py
├── auth_helpers.py
├── firebase_config.py
├── firebase_firestore.py
├── serviceAccount.json
├── icon.ico
├── requirements.txt
├── daily_check_<user_id>.json  ← Created at runtime
├── token.json                  ← Created at runtime
```
