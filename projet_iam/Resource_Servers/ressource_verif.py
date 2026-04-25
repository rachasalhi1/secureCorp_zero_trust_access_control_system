from crypto_rsa import encrypt, decrypt
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import time
ks="1234567"

def is_ticket_valid(ticket):
    current = time.time()

    if current > ticket["expiry"]:
        return False   # expired

    return True  

def verifying_data (encrypted_service_ticket,encrypted_authticator):
   used_authenticators = set()

   service_ticket=decrypt(encrypted_service_ticket,ks)
   validation=is_ticket_valid(service_ticket)
   if (validation==False):
     return False
   ks_session_key=service_ticket["ks_session_key"]
   authticator=decrypt(encrypted_authticator,ks_session_key)
   timestamp=authticator["timestamp"]
    #  Check timestamp freshness
    # checking the expiration
   if time.time() - timestamp > 60:
        return False
  
   # 5. Prevent replay (nonce or unique ID)
   auth_id = (authticator["username"], authticator["timestamp"])
   if auth_id in used_authenticators:
        return False

   used_authenticators.add(auth_id)
   encrypted_timestamp=encrypt(timestamp,ks_session_key)
   
  
   if authticator["username"] == service_ticket["username"]:
     return True, {
       "encrypted_timestamp":encrypted_timestamp
     }
      
def call_pdp(encrypted_service_ticket,encrypted_authticator) :
    service_ticket=decrypt(encrypted_service_ticket,ks)
    
    service_id=service_ticket["service"]
    ks_session_key=service_ticket["ks_session_key"]
    authticator=decrypt(encrypted_authticator,ks_session_key)
    username=authticator["username"]

      

    url = "http://localhost:5001" + "/decide "

    data = json.dumps({
        "user": username,
        "resource": service_id,
    }).encode()

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

    except Exception as e:
        return {"success": False, "message": str(e)}
    
   # return if access_granted or denied
   

    
            
