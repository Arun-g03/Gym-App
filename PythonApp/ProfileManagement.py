import tkinter as tk
from tkinter import ttk
from database_handler import Database_Handler  # Adjust import based on your folder structure




# ---------------------------
# Profile Management UI (for members)
# ---------------------------
class ProfileManagement:
    """
    Handles profile management functionality for members.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Gym App - Profile Management")
        self.db = Database_Handler()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Manage Your Profile", font=("Arial", 16)).pack(pady=10)

        ttk.Label(frame, text="Name").pack(anchor=tk.W)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Email").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(frame)
        self.email_entry.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Password").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)

        ttk.Button(frame, text="Update Profile", command=self.update_profile).pack(pady=10)

    def update_profile(self):
        print("Update profile information")
        # Implement profile update logic


