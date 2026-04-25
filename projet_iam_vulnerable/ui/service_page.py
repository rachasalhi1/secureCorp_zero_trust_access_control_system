
import tkinter as tk

window = tk.Tk()
window.title("SecureCorp")
window.geometry("300x300")

tk.Label(window, text="welcome ").pack(pady=5)

window.mainloop()
import tkinter as tk
def chosing_ressource_and_action():
    window = tk.Tk()
    window.title("SecureCorp Login")
    window.geometry("500x500")

    tk.Label(window, text="action").pack(pady=5)
    entry_username = tk.Entry(window)
    entry_username.pack()

   

    tk.Label(window, text="service").pack(pady=5)
    entry_service_id = tk.Entry(window)
    entry_service_id.pack()
    tk.Label(window, text="action").pack(pady=5)
    entry_username = tk.Entry(window)
    entry_username.pack()

   # tk.Button(window, text="Login", command=handle_login).pack(pady=20)

    window.mainloop()
def resource_access(service_id):
 window = tk.Tk()
 window.title("SecureCorp")
 window.geometry("300x300")

 tk.Label(window, text="welcome  service_id").pack(pady=5)

 window.mainloop()