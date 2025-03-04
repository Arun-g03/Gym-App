import database_handler


import tkinter as tk
from tkinter import ttk, messagebox
from database_handler import Database_Handler  # Adjust import based on your folder structure
 # Adjust import based on your folder structure


window_size = "512x384" #Size of the window

class Session:
    """ 
    Session object to store user session data.
    """
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role


    def __str__(self):
        return f"Session(user_id={self.user_id}, username={self.username}, role={self.role})"


def logout(self):
        """
        Logout the user and navigate to the login screen.
        outside class to reduce repetition
        Called by the logout button in the UI for all user types.
        """
        print("Logging out...")
        self.session = None
        self.master.destroy()
        root = tk.Tk()
        root.geometry(window_size)
        LoginUI(root)
        root.mainloop()

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
        ttk.Label(frame, text="Rusties Gym", font=("Arial", 16)).grid(row=0, column=0, pady=10)
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
# ---------------------------
# Signup UI
# ---------------------------
class SignupUI:
    """
    Signup UI class to handle user signup functionality.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Rusties Gym - Signup")
        self.db = Database_Handler()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Rusties Gym", font=("Arial", 16)).pack(pady=5)
        ttk.Label(frame, text="New Member - Signup", font=("Arial", 14)).pack(pady=5)

        # Name
        ttk.Label(frame, text="Name").pack(anchor=tk.W)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.pack(fill=tk.X, pady=5)

        # Email
        ttk.Label(frame, text="Email").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(frame)
        self.email_entry.pack(fill=tk.X, pady=5)

        # Password
        ttk.Label(frame, text="Password").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)

        # Subscription Plan Selection
        ttk.Label(frame, text="Select Subscription Plan").pack(anchor=tk.W)
        self.subscription_var = tk.StringVar()
        self.subscription_dropdown = ttk.Combobox(frame, textvariable=self.subscription_var, state="readonly")
        self.subscription_dropdown.pack(fill=tk.X, pady=5)

        # Populate dropdown with available subscription plans
        self.load_subscriptions()

        # Payment Method Selection
        ttk.Label(frame, text="Select Payment Method").pack(anchor=tk.W)
        self.payment_method_var = tk.StringVar(value="Credit Card")
        payment_methods = ["Credit Card", "PayPal", "Cash"]
        self.payment_dropdown = ttk.Combobox(frame, textvariable=self.payment_method_var, values=payment_methods, state="readonly")
        self.payment_dropdown.pack(fill=tk.X, pady=5)

        # Signup Button
        ttk.Button(frame, text="Signup", command=self.signup).pack(pady=10)
        ttk.Button(frame, text="Go to Login", command=self.go_to_login).pack(pady=5)

    def load_subscriptions(self):
        """ Load available subscription plans from the database """
        plans = self.db.get_all_subscriptions()  # Fetch plans from DB
        if plans:
            self.subscription_dropdown["values"] = [f"{plan[0]} - {plan[1]} (${plan[2]})" for plan in plans]
        else:
            self.subscription_dropdown["values"] = ["No plans available"]
        self.subscription_dropdown.current(0)  # Select first item by default

    def signup(self):
        """ Handles user signup and payment processing """
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        subscription_text = self.subscription_var.get()
        payment_method = self.payment_method_var.get()

        if not all([name, email, password, subscription_text]):
            messagebox.showerror("Error", "All fields must be filled out!")
            return

        # Extract subscription ID from dropdown value
        try:
            subscription_id = int(subscription_text.split(" - ")[0])  # Extracts the first part as ID
        except ValueError:
            messagebox.showerror("Error", "Invalid subscription selection!")
            return

        # Insert member into database
        member_id = self.db.insert_member(name, email, password, subscription_id)
        if member_id:
            # Fetch subscription price
            subscription_price = self.db.get_subscription_price(subscription_id)

            # Insert initial payment record
            self.db.insert_payment(member_id, subscription_price, payment_method, status="Paid")

            messagebox.showinfo("Success", "Signup successful! Payment recorded.")
            self.go_to_login()
        else:
            messagebox.showerror("Error", "Signup failed!")

    def go_to_login(self):
        """ Navigates to the Login UI """
        self.master.destroy()
        root = tk.Tk()
        root.geometry("512x384")
        LoginUI(root)
        root.mainloop()


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

class Trainer:
    """
    Handles trainer-specific functionality.
    Shows staff member specific information
    """
    def __init__(self, master, session):
        self.master = master
        self.master.title("Gym App - Trainer Dashboard")
        self.db = Database_Handler()
        self.session = session
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Trainer Dashboard", font=("Arial", 16)).pack(pady=10)

        # Display trainer's name
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM gym_staff WHERE id = ?", (self.session.user_id,))
        trainer_name = cursor.fetchone()[0]
        ttk.Label(frame, text=f"Welcome, {trainer_name}", font=("Arial", 12)).pack(pady=5)

        # Display hours worked this week
        cursor.execute("""
            SELECT SUM(
                ROUND(
                    (JULIANDAY(COALESCE(clock_out, datetime('now'))) - JULIANDAY(clock_in)) * 24
                )
            ) as hours
            FROM work_rota 
            WHERE staff_id = ? 
            AND date >= date('now', 'weekday 0', '-7 days')
            AND date < date('now', 'weekday 0', '+1 days')
        """, (self.session.user_id,))
        hours_worked = cursor.fetchone()[0] or 0
        

        # Check if trainer is currently clocked in
        cursor.execute(
            "SELECT clock_in FROM work_rota WHERE staff_id = ? AND date = date('now') AND clock_out IS NULL;",
            (self.session.user_id,)
        )
        clocked_in = cursor.fetchone() is not None
        status_text = "Currently clocked in" if clocked_in else "Currently clocked out"
        ttk.Label(frame, text=status_text, font=("Arial", 12)).pack(pady=5)
        ttk.Label(frame, text=f"Hours worked this week: {hours_worked}", font=("Arial", 12)).pack(pady=5)
        # Example: View assigned classes (this could be modified based on actual logic)
        ttk.Button(frame, text="View Assigned Classes", command=lambda: self.view_assigned_classes(self.session)).pack(pady=5)
        ttk.Button(frame, text="Log Work Hours", command=lambda: self.log_work_hours(self.session)).pack(pady=5)        
        ttk.Button(frame, text="Logout Staff", command=self.logout).pack(pady=10)

    def view_assigned_classes(self, session):
        print("Trainer: Viewing assigned classes")
        window = tk.Toplevel(self.master)
        window.title("Assigned Classes")
        window.geometry(window_size)
        
        # Create a Treeview for assigned classes (ID, Class Name, Schedule, Capacity, Description)
        columns = ("ID", "Class Name", "Schedule", "Capacity", "Description")
        tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Get the trainer's staff id from the session
        trainer_id = session.user_id  # Assumes session has attribute user_id
        
        try:
            cursor = self.db.conn.cursor()
            # Query classes where trainer_id matches the logged-in trainer
            cursor.execute("""
                SELECT id, class_name, schedule, capacity, description
                FROM classes
                WHERE trainer_id = ?;
            """, (trainer_id,))
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error loading assigned classes: {e}")


    def log_work_hours(self, session):
        """
        Log work hours for the currently logged-in staff.
        If the staff is not clocked in (no entry today with NULL clock_out), then clock them in.
        If they are already clocked in, clock them out by updating the record with the current time.
        
        :param session: Session object that contains user_id of the logged-in staff.
        """
        # Use the session object to get the staff member's id
        staff_id = session.user_id
        
        cursor = self.db.conn.cursor()
        # Check if there's an active (clocked in) entry for today.
        cursor.execute(
            "SELECT id, clock_in FROM work_rota WHERE staff_id = ? AND date = date('now') AND clock_out IS NULL;",
            (staff_id,)
        )
        active_entry = cursor.fetchone()
        
        if active_entry:
            # Staff is already clocked in; update the record with clock_out time.
            rota_id = active_entry[0]
            cursor.execute(
                "UPDATE work_rota SET clock_out = datetime('now') WHERE id = ?;",
                (rota_id,)
            )
            self.db.conn.commit()
            print(f"Clocked out successfully. Clock in was at {active_entry[1]}.")
        else:
            # Staff is not clocked in; insert a new record with clock_in time.
            cursor.execute(
                "INSERT INTO work_rota (staff_id, clock_in, date) VALUES (?, datetime('now'), date('now'));",
                (staff_id,)
            )
            self.db.conn.commit()
            print("Clocked in successfully.")


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



def initialise_database():
    """ Initialise the "database_handler" class and create tables if they don't exist """
    db_handler = database_handler.Database_Handler()
    db_handler.create_tables()

def main():
    """ Main function to start the application """
    # Initialise the database setup
    initialise_database()
    
    # Start the application with login UI
    root = tk.Tk()
    root.geometry(window_size)
    login_ui = LoginUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()