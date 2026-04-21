from crypto_rsa import encrypt, decrypt

ks=""
def verifying_data (encrypted_service_ticket,encrypted_authticator):
   service_ticket=decrypt(encrypted_service_ticket,ks)
   ks_session_key=service_ticket["ks_session_key"]
   authticator=decrypt(encrypted_authticator,ks_session_key)
   timestamp=authticator["timestamp"]
   encrypted_timestamp=encrypt( timestamp,ks_session_key)
   
    
   if authticator["username"] == service_ticket["username"]:
     return True, {
       "encrypted_timestamp":encrypted_timestamp
     }
      
     
            
            