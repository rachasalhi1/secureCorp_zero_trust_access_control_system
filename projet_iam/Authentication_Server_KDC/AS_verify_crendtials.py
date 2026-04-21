from crypto import hash_data
import json

Kc=""
Ktgs=""
#AS
with open("bdd/users.json", "r") as f:
    users = json.load(f)

def verify_credentials(username):
    if username not in users:
        return False, "User not found"

    kc = users[username]["password"]
    user_data = users[username]

    return True, {
        "username": username,
     
    }