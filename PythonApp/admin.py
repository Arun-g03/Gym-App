import tkinter as tk
from tkinter import ttk, messagebox
from database_handler import Database_Handler  # Adjust import based on your folder structure
from config import window_size
from Session import Session
from Trainer import Trainer
from UserDashboard import UserDashboard
from Signup import SignupUI

# ---------------------------
# Admin UI (for system administration)
# ---------------------------
class Admin:
    """
    Contains methods for managing members, staff, classes and subscriptions.
    """
    def __init__(self, master, session):
        self.master = master
        self.master.title("Gym App - Admin Dashboard")
        self.master.geometry(window_size)
        self.db = Database_Handler()
        self.session = session
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

        ttk.Button(frame, text="Manage Members", command=self.manage_members).pack(pady=5)
        ttk.Button(frame, text="Manage Staff", command=self.manage_staff).pack(pady=5)
        ttk.Button(frame, text="Manage Classes", command=self.manage_classes).pack(pady=5)
        ttk.Button(frame, text="Manage Subscriptions", command=self.manage_subscriptions).pack(pady=5)
        ttk.Button(frame, text="Logout", command=self.logout).pack(pady=10)

    def manage_members(self):
        print("Admin: Managing members")
        window = tk.Toplevel(self.master)
        window.title("Manage Members")
        window.geometry(window_size)
        
        columns = ("ID", "Name", "Email", "Billing Date", "Sign Up Date")
        tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_tree(tree, "SELECT id, name, email, billing_date, sign_up_date FROM members;")
        
        button_frame = ttk.Frame(window, padding="10")
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Edit Selected", command=lambda: self.edit_member(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=lambda: self.delete_member(tree)).pack(side=tk.LEFT, padx=5)
    
    def edit_member(self, tree):
        selected = tree.selection()
        if not selected:
            print("No member selected")
            return
        item = tree.item(selected[0])
        member_data = item['values']
        member_id = member_data[0]
        
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Member")
        edit_window.geometry("400x300")
        
        ttk.Label(edit_window, text="Name:").pack(anchor=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.pack(fill=tk.X, padx=10)
        name_entry.insert(0, member_data[1])
        
        ttk.Label(edit_window, text="Email:").pack(anchor=tk.W, padx=10, pady=5)
        email_entry = ttk.Entry(edit_window)
        email_entry.pack(fill=tk.X, padx=10)
        email_entry.insert(0, member_data[2])
        
        ttk.Label(edit_window, text="Password:").pack(anchor=tk.W, padx=10, pady=5)
        password_entry = ttk.Entry(edit_window, show="*")
        password_entry.pack(fill=tk.X, padx=10)
        
        def save_changes():
            new_name = name_entry.get()
            new_email = email_entry.get()
            new_password = password_entry.get()
            self.db.update_member(member_id, name=new_name, email=new_email, password=new_password)
            print("Member updated successfully.")
            edit_window.destroy()
            self.refresh_tree(tree, "SELECT id, name, email, billing_date, sign_up_date FROM members;")
        
        ttk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
    
    def delete_member(self, tree):
        selected = tree.selection()
        if not selected:
            print("No member selected")
            return
        item = tree.item(selected[0])
        member_id = item['values'][0]
        self.db.delete_member(member_id)
        print("Member deleted successfully.")
        self.refresh_tree(tree, "SELECT id, name, email, billing_date, sign_up_date FROM members;")
    
    def refresh_tree(self, tree, query):
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error refreshing tree: {e}")

    def manage_staff(self):
        print("Admin: Managing staff")
        window = tk.Toplevel(self.master)
        window.title("Manage Staff")
        window.geometry(window_size)
        
        columns = ("ID", "Name", "Role", "Salary", "Work Hours", "Contact", "Hire Date", "Termination Date")
        tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(window, padding="10")
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Add Staff", command=lambda: self.add_edit_staff_dialog(tree, edit=False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Staff", command=lambda: self.add_edit_staff_dialog(tree, edit=True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Staff", command=lambda: self.delete_staff_member(tree)).pack(side=tk.LEFT, padx=5)
        
        self.refresh_staff_tree(tree)
    
    def refresh_staff_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT id, name, role, salary, work_hours, contact_number, hire_date, termination_date FROM gym_staff;")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error loading staff: {e}")
    
    def add_edit_staff_dialog(self, tree, edit=False):
        dialog = tk.Toplevel(self.master)
        dialog.title("Add Staff" if not edit else "Edit Staff")
        dialog.geometry("400x600")
        
        if edit:
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a staff member to edit")
                dialog.destroy()
                return
            item = tree.item(selected[0])
            values = item['values']
            staff_id = values[0]
        
        fields = {}
        
        for field in ["Name", "Role", "Salary", "Contact Number"]:
            ttk.Label(dialog, text=f"{field}:").pack(pady=5)
            entry = ttk.Entry(dialog)
            entry.pack(fill=tk.X, padx=10)
            fields[field.lower().replace(" ", "_")] = entry
        
        ttk.Label(dialog, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.pack(fill=tk.X, padx=10)
        
        ttk.Label(dialog, text="Hire Date (YYYY-MM-DD):").pack(pady=5)
        hire_date_entry = ttk.Entry(dialog)
        hire_date_entry.pack(fill=tk.X, padx=10)
        
        ttk.Label(dialog, text="Termination Date (YYYY-MM-DD, optional):").pack(pady=5)
        termination_date_entry = ttk.Entry(dialog)
        termination_date_entry.pack(fill=tk.X, padx=10)
        
        if edit:
            staff = self.db.get_staff(staff_id)
            fields["name"].insert(0, staff[2])
            fields["role"].insert(0, staff[3])
            fields["salary"].insert(0, staff[4])
            fields["contact_number"].insert(0, staff[6])
            hire_date_entry.insert(0, staff[7])
            if staff[8]:
                termination_date_entry.insert(0, staff[8])
        
        def save_staff():
            try:
                name = fields["name"].get()
                role = fields["role"].get()
                salary = float(fields["salary"].get())
                contact = fields["contact_number"].get()
                hire_date = hire_date_entry.get()
                termination_date = termination_date_entry.get() if termination_date_entry.get() else None
                
                if edit:
                    self.db.update_staff(staff_id, name=name, role=role, salary=salary,
                                       contact_number=contact, hire_date=hire_date,
                                       termination_date=termination_date)
                else:
                    password = password_entry.get()
                    self.db.insert_staff(name, role, salary, contact, hire_date, password,
                                       termination_date=termination_date)
                
                self.refresh_staff_tree(tree)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", "Please ensure all fields are filled correctly")
        
        ttk.Button(dialog, text="Save", command=save_staff).pack(pady=10)
    
    def delete_staff_member(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this staff member?"):
            item = tree.item(selected[0])
            staff_id = item['values'][0]
            self.db.delete_staff(staff_id)
            self.refresh_staff_tree(tree)
    
    def manage_classes(self):
        print("Admin: Managing classes")
        window = tk.Toplevel(self.master)
        window.title("Manage Classes")
        window.geometry(window_size)
        
        columns = ("ID", "Class Name", "Schedule", "Capacity", "Description", "Trainer Assigned")
        tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)
        
        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Class", command=lambda: self.add_edit_class_dialog(tree, edit=False)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Class", command=lambda: self.add_edit_class_dialog(tree, edit=True)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Class", command=lambda: self.delete_class(tree)).pack(side=tk.LEFT, padx=5)
        
        self.refresh_classes_tree(tree)
    
    def refresh_classes_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT id, class_name, schedule, capacity, description, trainer_id 
                FROM classes;
            """)
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error loading classes: {e}")
    
    def add_edit_class_dialog(self, tree, edit=False):
        dialog = tk.Toplevel(self.master)
        dialog.title("Add Class" if not edit else "Edit Class")
        dialog.geometry("512x512")
        
        if edit:
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a class to edit")
                dialog.destroy()
                return
            item = tree.item(selected[0])
            values = item['values']
        
        tk.Label(dialog, text="Class Name:").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack()
        
        tk.Label(dialog, text="Schedule:").pack(pady=5)
        days_frame = tk.Frame(dialog)
        days_frame.pack(pady=5)
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_vars = []
        for day in days:
            var = tk.BooleanVar()
            day_vars.append(var)
            tk.Checkbutton(days_frame, text=day, variable=var).pack(side=tk.LEFT)
        
        time_frame = tk.Frame(dialog)
        time_frame.pack(pady=5)
        tk.Label(time_frame, text="Start Time:").pack(side=tk.LEFT)
        start_time = tk.Entry(time_frame, width=10)
        start_time.pack(side=tk.LEFT, padx=5)
        tk.Label(time_frame, text="End Time:").pack(side=tk.LEFT)
        end_time = tk.Entry(time_frame, width=10)
        end_time.pack(side=tk.LEFT, padx=5)
        
        tk.Label(dialog, text="Capacity:").pack(pady=5)
        capacity_entry = tk.Entry(dialog)
        capacity_entry.pack()
        
        tk.Label(dialog, text="Description:").pack(pady=5)
        description_text = tk.Text(dialog, height=4)
        description_text.pack()
        
        tk.Label(dialog, text="Select Trainers:").pack(pady=5)
        trainer_listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE, height=5)
        trainer_listbox.pack()
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, name FROM gym_staff WHERE role = 'Trainer';")
        trainers = cursor.fetchall()
        for trainer in trainers:
            trainer_listbox.insert(tk.END, f"{trainer[0]} - {trainer[1]}")
        
        if edit:
            name_entry.insert(0, values[1])
            schedule = values[2].split()
            if len(schedule) >= 2:
                times = schedule[-1].split('-')
                if len(times) == 2:
                    start_time.insert(0, times[0])
                    end_time.insert(0, times[1])
                for day in schedule[:-1]:
                    if day in days:
                        day_vars[days.index(day)].set(True)
            capacity_entry.insert(0, values[3])
            description_text.insert("1.0", values[4])
            trainer_ids = values[5].split(',') if values[5] else []
            for i, trainer in enumerate(trainers):
                if str(trainer[0]) in trainer_ids:
                    trainer_listbox.selection_set(i)
        
        def save_class():
            name = name_entry.get()
            selected_days = [days[i] for i, var in enumerate(day_vars) if var.get()]
            schedule = f"{' '.join(selected_days)} {start_time.get()}-{end_time.get()}"
            capacity = capacity_entry.get()
            description = description_text.get("1.0", tk.END).strip()
            selected_trainers = [trainers[idx][0] for idx in trainer_listbox.curselection()]
            trainer_ids = ','.join(map(str, selected_trainers))
            
            try:
                if edit:
                    self.db.conn.execute("""
                        UPDATE classes 
                        SET class_name=?, schedule=?, capacity=?, description=?, trainer_id=? 
                        WHERE id=?""", (name, schedule, capacity, description, trainer_ids, values[0]))
                else:
                    self.db.conn.execute("""
                        INSERT INTO classes (class_name, schedule, capacity, description, trainer_id)
                        VALUES (?, ?, ?, ?, ?)""", (name, schedule, capacity, description, trainer_ids))
                self.db.conn.commit()
                dialog.destroy()
                self.refresh_class_tree(tree)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save class: {str(e)}")

        tk.Button(dialog, text="Save", command=save_class).pack(pady=10)


    def manage_subscriptions(self):
        print("Admin: Managing subscriptions")
        # Implement navigation to a subscription management UI
