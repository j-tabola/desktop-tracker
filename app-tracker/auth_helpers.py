from firebase_firestore import get_db
from datetime import datetime
import json
import keyring
import os

db = get_db()

def create_user_document(user_id, email):
    user_ref = db.collection("Users").document(user_id)
    if not user_ref.get().exists:
        user_ref.set({
            "email": email,
            "createdAt": datetime.utcnow()
        })
        # ADDS SAMPLE LINK ON ACCOUNT CREATION
        #
        # links_ref = user_ref.collection("links")
        # links_ref.document("placeholder").set({
        #     "name": "Sample Link",
        #     "url": "https://example.com",
        #     "createdAt": datetime.utcnow()
        # })

def create_cache_login(email, password):
    with open("token.json", "w") as f:
        json.dump({"email": email}, f)
    keyring.set_password("app_tracker", email, password)

def load_cached_login():
        if not os.path.exists("token.json"):
            return None

        with open("token.json", "r") as f:
            data = json.load(f)
            email = data.get("email")
            if email:
                password = keyring.get_password("app_tracker", email)
                if password:
                    return email, password
        return None