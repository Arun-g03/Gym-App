import tkinter as tk
from tkinter import ttk, messagebox
from database_handler import Database_Handler  # Adjust import based on your folder structure
from config import window_size






# ---------------------------
# Signup UI
# ---------------------------
class SignupUI:
    """
    Signup UI class to handle user signup functionality.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("World Gym - Signup")
        self.db = Database_Handler()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="World Gym", font=("Arial", 16)).pack(pady=5)
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
        from Login import LoginUI
        """ Navigates to the Login UI """
        self.master.destroy()
        root = tk.Tk()
        root.geometry("512x384")
        LoginUI(root)
        root.mainloop()


