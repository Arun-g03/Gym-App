import tkinter as tk
from tkinter import ttk
from database_handler import Database_Handler  # Adjust import based on your folder structure
from config import window_size





# ---------------------------
# Class Selection UI (for members)
# ---------------------------
class ClassSelection:
    """
    Class = a class that a member can enroll in like yoga, pilates, etc.


    Handles class selection functionality for members.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Gym App - Class Selection")
        self.db = Database_Handler()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Available Classes", font=("Arial", 16)).pack(pady=10)

        # Treeview to display available classes
        self.class_tree = ttk.Treeview(frame, columns=("ID", "Class Name", "Schedule", "Capacity"), show="headings")
        self.class_tree.heading("ID", text="ID")
        self.class_tree.heading("Class Name", text="Class Name")
        self.class_tree.heading("Schedule", text="Schedule")
        self.class_tree.heading("Capacity", text="Capacity")
        self.class_tree.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Sign Up for Selected Class", command=self.sign_up_class).pack(pady=10)
        self.load_classes()

    def load_classes(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT id, class_name, schedule, capacity FROM classes")
            rows = cursor.fetchall()
            for row in rows:
                self.class_tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error loading classes: {e}")

    def sign_up_class(self):
        print("Sign up for selected class")
        # Implement sign-up logic here

