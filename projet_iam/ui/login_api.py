
import urllib.request
import json

Login_URL = "http://localhost:5000"
service_request_URL="http://localhost:6000"
resource_server_request_URL="http://localhost:7000"
def login_request(username):
    url = Login_URL + "/login"

    data = json.dumps({
        "username": username,
    }).encode()

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

    except Exception as e:
        return {"success": False, "message": str(e)}





def request_tgs(encryped_tgt,service_id,encrypted_authticator):
   url = service_request_URL + "/ticket_request"
   data = json.dumps({
        "encryped_tgt": encryped_tgt,
         "service_id": service_id,
          "encrypted_authticator": encrypted_authticator,
    }).encode()
   req = urllib.request.Request(url, data=data, method="POST")
   req.add_header("Content-Type", "application/json")

   try:
        response = urllib.request.urlopen(req,timeout=5)
        return json.loads(response.read().decode())

   except Exception as e:
        return {"success": False, "message": str(e)}

def request_ressource_service(encrypted_service_ticket,encrypted_authticator):
    url = resource_server_request_URL + "/service_request"
    data = json.dumps({
        "encrypted_service_ticket": encrypted_service_ticket,
        "encrypted_authticator": encrypted_authticator,
     }).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        response = urllib.request.urlopen(req,timeout=5)
        return json.loads(response.read().decode())

    except Exception as e:
        return {"success": False, "message": str(e)}