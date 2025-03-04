import tkinter as tk
from tkinter import ttk
from database_handler import Database_Handler  # Adjust import based on your folder structure
from config import window_size
from Session import Session
from admin import Admin
from Trainer import Trainer
from UserDashboard import UserDashboard
from Signup import SignupUI


# ---------------------------
# Login UI
# ---------------------------
class LoginUI:
    """
    Login UI class to handle user login functionality.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Gym App - Login")
        self.db = Database_Handler()
        self.create_widgets()

    def create_widgets(self):
        # Main frame with weight configuration
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(self.master, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure frame grid weights
        frame.grid_columnconfigure(0, weight=1)
        ttk.Label(frame, text="World Gym", font=("Arial", 16)).grid(row=0, column=0, pady=10)
        # Header
        ttk.Label(frame, text="Login", font=("Arial", 16)).grid(row=1, column=0, pady=10)
        
        # Email field
        ttk.Label(frame, text="Email").grid(row=1, column=0, sticky="w")
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Password field
        ttk.Label(frame, text="Password").grid(row=3, column=0, sticky="w")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=4, column=0, sticky="ew", pady=5)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, sticky="ew", pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Button(button_frame, text="Login", command=self.login).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Staff Login", command=self.staff_login).grid(row=0, column=1, padx=5)
        
        # Signup button
        ttk.Button(frame, text="Go to Signup", command=self.go_to_signup).grid(row=6, column=0, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate credentials for a member (or staff)
        user = self.db.validate_login(username, password, login_type="member")
        if user:
            # Create a session object for the logged-in user
            session = Session(user["id"], user["username"], user["role"])
            print("Login successful:", session)
            
            self.master.destroy()  # Close the login window
            root = tk.Tk()
            
            if session.role == "admin":
                Admin(root, session).run()         # Launch Admin Dashboard
            elif session.role == "trainer":
                Trainer(root, session).run()         # Launch Trainer Dashboard
            else:
                UserDashboard(root, session).run()       # Launch Member Dashboard
        else:
            print("Invalid credentials")


    def staff_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate as a staff login only
        user = self.db.validate_login(username, password, login_type="staff")
        if user:
            role = user.get("role")
            session = Session(user["id"], user["username"], user["role"])
            self.master.destroy()
            
            root = tk.Tk()
            root.geometry(window_size)
            if role == "admin":
                Admin(root, session).run()
            elif role == "trainer":
                Trainer(root, session).run()        
            else:
                print("Invalid staff credentials")

    def go_to_signup(self):
        # For navigation: destroy current widgets or open a new window
        print("Navigating to Signup UI")
        self.master.destroy()  # or implement frame switching logic
        root = tk.Tk()
        root.geometry(window_size)
        SignupUI(root)
        root.mainloop()

