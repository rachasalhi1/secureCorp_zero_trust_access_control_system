from .crypto_rsa import encrypt, decrypt
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import time
ks=""
def verifying_data (service_ticket,encrypted_authticator):
   #service_ticket=decrypt(encrypted_service_ticket,ks)
   ks_session_key=service_ticket["ks_session_key"]
   authticator=decrypt(encrypted_authticator,ks_session_key)
   timestamp=authticator["timestamp"]
   encrypted_timestamp=encrypt( timestamp,ks_session_key)
   
    
   if authticator["username"] == service_ticket["username"]:
     return True, {
       "encrypted_timestamp":encrypted_timestamp
     }
      
     # herre we call the pdp
def call_pdp(service_ticket,encrypted_authticator) :
    #service_ticket=decrypt(encrypted_service_ticket,ks)
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
   

    
                

    
            