from firebase_firestore import get_db
from datetime import datetime

db = get_db()

def get_links(user_id):
    ref = db.collection("Users").document(user_id).collection("links")
    docs = ref.stream()
    return [(doc.id, doc.to_dict()) for doc in docs]

def add_link(user_id, name, url):
    ref = db.collection("Users").document(user_id).collection("links")
    ref.add({
        "name": name,
        "url": url,
        "createdAt": datetime.utcnow()
    })

def delete_link(user_id, link_id):
    db.collection("Users").document(user_id).collection("links").document(link_id).delete()
