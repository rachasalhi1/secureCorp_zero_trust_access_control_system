import time
import hashlib
from .crypto_rsa import decrypt, encrypt
TICKET_LIFETIME = 300
ktgs=""
ks=""
ks_session_key=""
def verfifying_tgt_and_authnticator(tgt,encrypted_authticator):
 # tgt=decrypt(encryped_tgt,ktgs)
  k_u_tgs=tgt["key_user_tgs"]
  authticator=decrypt(encrypted_authticator,k_u_tgs)
  username_from_auth=authticator["username"]
  username_fromtgt=tgt["username"]
  if username_from_auth==username_fromtgt:
   return True





def create_service_ticket(tgt, service_id):

   # tgt=decrypt(encrypted_tgt,ktgs)
    service_ticket = {
        "username":tgt["username"],
        "service": service_id,
        #session key betweeen client and service 
        "ks_session_key":ks_session_key,
        "expiry": time.time() + TICKET_LIFETIME
    }
    #encrypted_service_ticket=encrypt(service_ticket,ks)
    k_u_tgs=tgt["key_user_tgs"]
    encrypted_ks_session_key=encrypt(ks_session_key,k_u_tgs)
    
    
    return {
    
        #"encrypted_service_ticket": encrypted_service_ticket,
        "service_ticket":service_ticket,
        "encrypted_ks_session_key":encrypted_ks_session_key
    }