from crypto import hash_data
import json

Kc=""
Ktgs=""
#AS
with open("bdd/users.json", "r") as f:
    db = json.load(f)
    
def verify_credentials(username):
    users = db["users"] 
    if username not in users:
        return False, "User not found"
    user_data = users[username]

    kc = user_data["password_hash"]
   
  

    return True, {
        "username": username,
     
    }
