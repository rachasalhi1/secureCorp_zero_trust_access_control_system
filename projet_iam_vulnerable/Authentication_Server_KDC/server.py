from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from .AS_verify_crendtials import  verify_credentials
from .AS_issuing_TGT import create_tgt
from .TGS import verfifying_tgt_and_authnticator
from .TGS import create_service_ticket
class KDCServer_AS(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/login":

           
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)

            username = data["username"]
          #  hashed_password = data["hashed_password"]
            success, result = verify_credentials(username)
            print(username)
            if not success:
                response = {
                    "success": False,
                    "message": result
                }
            else:
               
                #session_k_u_tgs_encryp,encryped_tgt = create_tgt(result)
                session_k_u_tgs_encryp,tgt = create_tgt(result)
                response = {
                    "success": True,
                     "session_k_u_tgs_encryp":session_k_u_tgs_encryp,
                   # "encrypted_tgt": encryped_tgt
                   "tgt":tgt
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())



class KDCServer_TGS(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/request-ticket":

            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)
            
        
            tgt = data["tgt"]
            service_id= data ["service_id"]
            encrypted_authticator= data ["encrypted_authticator"]
            #to change from here 
            result=verfifying_tgt_and_authnticator(tgt,encrypted_authticator)
            if result==True :
                 result1 = create_service_ticket(tgt,service_id)
                
                 
                        
            
            response = {
            "success": True,
            "service_ticket": result1["service_ticket"],
            "encrypted_ks_session_key":result1["encrypted_ks_session_key"]
               }


server_AS= HTTPServer(("localhost", 5000), KDCServer_AS)
print("KDC running on /login ")
server_AS.serve_forever()

server_TGS= HTTPServer(("localhost", 6000), KDCServer_TGS)
print("KDC running on /service_ticket ")
server_TGS.serve_forever()

