import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import messagebox
from .login_api import login_request
from .login_api import request_tgs 
from Authentication_Server_KDC.crypto import hash_data 
from Authentication_Server_KDC.crypto_rsa import encrypt, decrypt
from .service_page import resource_access
from .login_api import request_ressource_service
import time
def handle_login():
    username = entry_username.get()
    password = entry_password.get()
    service_id=entry_service_id.get()
    hashed_password = hash_data(password)
    result = login_request(username)
    if (result['success']==True ):
     session_k_u_tgs_encrypt= result["session_k_u_tgs_encryp"]
     tgt=result["tgt"]
     k_u_tgs=decrypt(session_k_u_tgs_encrypt,hashed_password)
       
     messagebox.showinfo("Success", "Login successful ")
        # demande to tgs
     timestamp=time.time()
     authticator= {"username":username, "timestamp":timestamp}
     encrypted_authticator=encrypt(authticator,k_u_tgs)
     response=request_tgs(tgt,service_id,encrypted_authticator)
     
          #  "encrypted_service_ticket": r
          #  "encrypted_ks_session_key":r
     encrypted_ks_session_key=response["encrypted_ks_session_key"]  
     ks_session_key=decrypt(encrypted_ks_session_key,k_u_tgs)      
     if response["success"]==True :

        new_authticator={"username":username,"timestamp":time.time}
        encrypted_authticator =encrypt(new_authticator,ks_session_key)
        result3=request_ressource_service(response["service_ticket"],encrypted_authticator)
        
        if result3["success"]==True:
           timestamp=decrypt(result3["encrypted_timestamp"],ks_session_key)
           if timestamp==new_authticator[timestamp] :
              print("u logged succesfully welcome")
              resource_access(service_id)
              #have to display the service
           else:
            messagebox.showerror("Error", result.get("message", "Login failed"))
        else:
           messagebox.showerror("Error", result.get("message", "Login failed"))
     else:
         messagebox.showerror("Error", result.get("message", "Login failed"))
    else:
        messagebox.showerror("Error", result.get("message", "Login failed"))

 

window = tk.Tk()
window.title("SecureCorp Login")
window.geometry("500x500")

tk.Label(window, text="Username").pack(pady=5)
entry_username = tk.Entry(window)
entry_username.pack()

tk.Label(window, text="Password").pack(pady=5)
entry_password = tk.Entry(window, show="*")
entry_password.pack()

tk.Label(window, text="service").pack(pady=5)
entry_service_id = tk.Entry(window)
entry_service_id.pack()


tk.Button(window, text="Login", command=handle_login).pack(pady=20)

window.mainloop()

import sys
print(sys.path)