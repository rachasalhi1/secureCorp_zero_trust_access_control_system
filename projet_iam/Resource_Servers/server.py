from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from ressource_verif import verifying_data
class RessourceServer(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/service_request":

           
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)
            encrypted_service_ticket=data[ "encrypted_service_ticket"]
       
            encrypted_authticator=data["encrypted_authticator"] 
            result,respons=verifying_data(encrypted_service_ticket, encrypted_authticator)
           
            if result==True :
                response = {
                    "success": True,
                     "encrypted_timestamp":respons["encrypted_timestamp"]
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

RessourceServer= HTTPServer(("localhost", 7000), RessourceServer)
print("RessourceServer running on /service_request ")
RessourceServer.serve_forever()
