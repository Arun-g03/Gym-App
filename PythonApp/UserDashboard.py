import tkinter as tk
from tkinter import ttk



# ---------------------------
# Dashboard UI
# ---------------------------
class UserDashboard:
    """
    User Dashboard UI class.
    Handles user dashboard functionality.
    """
    def __init__(self, master, session):
        self.master = master
        self.master.title("Gym App - User Dashboard")
        self.create_widgets()
        self.session = session

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Dashboard", font=("Arial", 16)).pack(pady=10)

        ttk.Button(frame, text="Profile Management", command=self.open_profile_management).pack(pady=5)
        ttk.Button(frame, text="Class Selection", command=self.open_class_selection).pack(pady=5)
        ttk.Button(frame, text="Class Management", command=self.open_class_management).pack(pady=5)
        ttk.Button(frame, text="Logout", command=self.logout).pack(pady=10)

    def open_profile_management(self):
        print("Opening Profile Management UI")
        # Implement navigation logic to ProfileManagementUI

    def open_class_selection(self):
        print("Opening Class Selection UI")
        # Implement navigation logic to ClassSelectionUI

    def open_class_management(self):
        print("Opening Class Management UI")
        # Implement navigation logic to ClassManagementUI


