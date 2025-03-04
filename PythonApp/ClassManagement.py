import tkinter as tk
from tkinter import ttk
from database_handler import Database_Handler  # Adjust import based on your folder structure



# ---------------------------
# Class Management UI (for staff)
# ---------------------------
class ClassManagement:
    """
    Handles class management functionality for staff.
    A class is something that a member can enroll in like yoga, pilates, etc.
    
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Gym App - Class Management")
        self.db = Database_Handler()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Manage Classes", font=("Arial", 16)).pack(pady=10)

        ttk.Button(frame, text="Add New Class", command=self.add_class).pack(pady=5)
        ttk.Button(frame, text="Edit Selected Class", command=self.edit_class).pack(pady=5)
        ttk.Button(frame, text="Delete Selected Class", command=self.delete_class).pack(pady=5)

        # Treeview to display classes
        self.class_tree = ttk.Treeview(frame, columns=("ID", "Class Name", "Schedule", "Capacity", "Description"), show="headings")
        self.class_tree.heading("ID", text="ID")
        self.class_tree.heading("Class Name", text="Class Name")
        self.class_tree.heading("Schedule", text="Schedule")
        self.class_tree.heading("Capacity", text="Capacity")
        self.class_tree.heading("Description", text="Description")
        self.class_tree.pack(fill=tk.BOTH, expand=True)
        self.load_classes()

    def load_classes(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT id, class_name, schedule, capacity, description FROM classes")
            rows = cursor.fetchall()
            for row in rows:
                self.class_tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error loading classes: {e}")

    def add_class(self):
        print("Add new class")
        # Implement adding a class

    def edit_class(self):
        print("Edit selected class")
        # Implement editing a class
 
    def delete_class(self):
        print("Delete selected class")
        # Implement deleting a class



