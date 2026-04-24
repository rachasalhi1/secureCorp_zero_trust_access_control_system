import time
import hashlib
from crypto_rsa import encrypt , decrypt
import json
from bdd.manager_bdd import get_user_by_username
from bdd.manager_bdd import get_password_hash
K_u_tgs=""
ktgs=""
  
TICKET_LIFETIME = 300
def create_tgt(user_info):
    username=user_info["username"]

   # with open("bdd/users.json", "r") as f:
    # users = json.load(f)
    #kc= users["username"]["password_hash"]
    
    kc=get_password_hash(username)
    A=encrypt(K_u_tgs, kc)
    tgt = {
        "username": user_info["username"],
        "expiry": time.time() + TICKET_LIFETIME,
        # session key between client and tgs
        "key_user_tgs":K_u_tgs
    }

    # encrypt tgt with secret key of tgs
    encrypted_tgt =encrypt(tgt,ktgs)
   
    return {
        "A":A,
        "encrypted_tgt": encrypted_tgt,
    }




