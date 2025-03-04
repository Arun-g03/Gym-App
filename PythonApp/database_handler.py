import sqlite3

class Database_Handler:
    def __init__(self, db_file="gym_database.db"):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.create_tables()

    def create_connection(self):
        """
        Create a database connection to the SQLite database specified by db_file.
        Returns the connection object.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(f"Connected to SQLite database at {self.db_file}.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return conn

    def create_tables(self):
        """
        Create tables for members, classes, gym_staff, subscriptions, work_rota, and admin.
        """
        try:
            cursor = self.conn.cursor()

            # Create table for gym members
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    subscription_id INTEGER,
                    billing_date DATE NOT NULL,  -- Member-specific billing date
                    Sign_up_Date DATE NOT NULL,  -- Member-specific sign-up date
                    FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
                );
            """)

            # Create table for gym classes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_name TEXT NOT NULL,
                    schedule TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    Attendance_count INTEGER DEFAULT 0,
                    description TEXT,
                    trainer_id INTEGER,  -- Assigned trainer (staff_id)
                    FOREIGN KEY (trainer_id) REFERENCES gym_staff (id)
                );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date DATE NOT NULL,
                payment_method TEXT NOT NULL,  -- e.g., "Credit Card", "PayPal", "Cash"
                status TEXT NOT NULL DEFAULT "Pending",  -- "Paid", "Pending", "Failed"
                transaction_id TEXT UNIQUE,  -- Optional for tracking transactions
                FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE
            );
            """)



            # Create table for gym staff (all employees including trainers, receptionists, etc.)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gym_staff (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER,  -- Optional, if staff are also registered as members
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,  -- e.g., "Trainer", "Receptionist", "Manager"
                    salary REAL NOT NULL,
                    work_hours REAL DEFAULT 0.0,  -- Applicable to all staff for tracking hours worked
                    contact_number TEXT,
                    hire_date DATE NOT NULL,
                    termination_date DATE,
                    password TEXT,
                    FOREIGN KEY (member_id) REFERENCES members (id)
                );
            """)

            # Create table for subscriptions (catalog of available subscription plans)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan TEXT NOT NULL,  -- Identifier for the subscription type (e.g., "Basic", "Extra")
                    price REAL NOT NULL  -- The cost associated with this subscription plan
                );
            """)

            # Create table for work rota (clocking in/out history for staff)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS work_rota (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    staff_id INTEGER NOT NULL,
                    clock_in DATETIME NOT NULL,
                    clock_out DATETIME,
                    date DATE NOT NULL,
                    FOREIGN KEY (staff_id) REFERENCES gym_staff (id)
                );
            """)

            # Create table for admin
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                );
            """)

            # Insert default admin user
            cursor.execute("""
                INSERT OR IGNORE INTO admin (username, password)
                VALUES ('admin', 'admin');
            """)

            # Commit changes
            self.conn.commit()
            print("All tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def validate_login(self, username, password, login_type="member"):
        """
        Validate login credentials for any user type (admin, staff, or member).
        Checks in the following order: admin > staff > member.
        
        For admin login, 'username' is used as is.
        For staff login, 'username' represents the staff's name.
        For member login, 'username' is the member's email.
        
        :param username: Username (or email for members).
        :param password: The password to validate.
        :param login_type: "member" (default) for normal login, "staff" for staff login.
        :return: A dictionary with user details and role if valid, else None.
                For example: {"id": 1, "username": "john@example.com", "role": "member"}
        """
        cursor = self.conn.cursor()
        
        # 1. Check the admin table first.
        cursor.execute("SELECT id FROM admin WHERE username = ? AND password = ?;", (username, password))
        admin = cursor.fetchone()
        if admin:
            return {"id": admin[0], "username": username, "role": "admin"}
        
        if login_type == "staff":
            # 2. For staff login, check the gym_staff table using the staff's name and password.
            cursor.execute("SELECT id, role FROM gym_staff WHERE name = ? AND password = ?;", (username, password))
            staff = cursor.fetchone()
            if staff:
                return {"id": staff[0], "username": username, "role": staff[1].lower()}
            else:
                return None
        else:
            # 3. For member login, check the members table using email and password.
            cursor.execute("SELECT id FROM members WHERE email = ? AND password = ?;", (username, password))
            member = cursor.fetchone()
            if not member:
                return None  # No member found, so invalid credentials.
            
            member_id = member[0]
            # 4. Check if this member is also a staff member.
            cursor.execute("SELECT role FROM gym_staff WHERE member_id = ?;", (member_id,))
            staff = cursor.fetchone()
            if staff:
                return {"id": member_id, "username": username, "role": staff[0].lower()}
            else:
                return {"id": member_id, "username": username, "role": "member"}




    # ------------------------------
    # CRUD Operations for Members
    # ------------------------------
    def insert_member(self, name, email, password, subscription_id=None):
        """
        Inserts a new member into the database.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO members (name, email, password, subscription_id, sign_up_date)
                VALUES (?, ?, ?, ?, date('now'));
            """, (name, email, password, subscription_id))
            self.conn.commit()
            print("Member inserted successfully.")
            return cursor.lastrowid  # Return the newly created member ID
        except sqlite3.Error as e:
            print(f"Error inserting member: {e}")
            return None


    def get_member(self, member_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM members WHERE id = ?;", (member_id,))
            member = cursor.fetchone()
            return member
        except sqlite3.Error as e:
            print(f"Error retrieving member: {e}")
            return None

    def update_member(self, member_id, name=None, email=None, password=None, subscription_id=None):
        try:
            cursor = self.conn.cursor()
            fields = []
            params = []
            if name:
                fields.append("name = ?")
                params.append(name)
            if email:
                fields.append("email = ?")
                params.append(email)
            if password:
                fields.append("password = ?")
                params.append(password)
            if subscription_id is not None:
                fields.append("subscription_id = ?")
                params.append(subscription_id)
            params.append(member_id)

            query = f"UPDATE members SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, params)
            self.conn.commit()
            print("Member updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating member: {e}")

    def delete_member(self, member_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM members WHERE id = ?;", (member_id,))
            self.conn.commit()
            print("Member deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting member: {e}")

    # ------------------------------
    # CRUD Operations for Classes
    # ------------------------------
    def insert_class(self, class_name, schedule, capacity, description=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO classes (class_name, schedule, capacity, description)
                VALUES (?, ?, ?, ?);
            """, (class_name, schedule, capacity, description))
            self.conn.commit()
            print("Class inserted successfully.")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting class: {e}")
            return None

    def get_class(self, class_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM classes WHERE id = ?;", (class_id,))
            gym_class = cursor.fetchone()
            return gym_class
        except sqlite3.Error as e:
            print(f"Error retrieving class: {e}")
            return None

    def update_class(self, class_id, class_name=None, schedule=None, capacity=None, description=None):
        try:
            cursor = self.conn.cursor()
            fields = []
            params = []
            if class_name:
                fields.append("class_name = ?")
                params.append(class_name)
            if schedule:
                fields.append("schedule = ?")
                params.append(schedule)
            if capacity is not None:
                fields.append("capacity = ?")
                params.append(capacity)
            if description is not None:
                fields.append("description = ?")
                params.append(description)
            params.append(class_id)

            query = f"UPDATE classes SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, params)
            self.conn.commit()
            print("Class updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating class: {e}")

    def delete_class(self, class_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM classes WHERE id = ?;", (class_id,))
            self.conn.commit()
            print("Class deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting class: {e}")

    # ------------------------------
    # CRUD Operations for Gym Staff
    # ------------------------------
    def insert_staff(self, name, role, salary, contact_number, hire_date, password, member_id=None, work_hours=0.0, termination_date=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO gym_staff (member_id, name, role, salary, work_hours, contact_number, hire_date, termination_date, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (member_id, name, role, salary, work_hours, contact_number, hire_date, termination_date, password))
            self.conn.commit()
            print("Staff inserted successfully.")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting staff: {e}")
            return None
    def get_staff(self, staff_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM gym_staff WHERE id = ?;", (staff_id,))
            staff = cursor.fetchone()
            return staff
        except sqlite3.Error as e:
            print(f"Error retrieving staff: {e}")
            return None

    def update_staff(self, staff_id, name=None, role=None, salary=None, work_hours=None, contact_number=None, hire_date=None, termination_date=None):
        try:
            cursor = self.conn.cursor()
            fields = []
            params = []
            if name:
                fields.append("name = ?")
                params.append(name)
            if role:
                fields.append("role = ?")
                params.append(role)
            if salary is not None:
                fields.append("salary = ?")
                params.append(salary)
            if work_hours is not None:
                fields.append("work_hours = ?")
                params.append(work_hours)
            if contact_number:
                fields.append("contact_number = ?")
                params.append(contact_number)
            if hire_date:
                fields.append("hire_date = ?")
                params.append(hire_date)
            if termination_date is not None:
                fields.append("termination_date = ?")
                params.append(termination_date)
            params.append(staff_id)

            query = f"UPDATE gym_staff SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, params)
            self.conn.commit()
            print("Staff updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating staff: {e}")

    def delete_staff(self, staff_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM gym_staff WHERE id = ?;", (staff_id,))
            self.conn.commit()
            print("Staff deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting staff: {e}")

    # ------------------------------
    # CRUD Operations for Subscriptions
    # ------------------------------
    def insert_subscription(self, plan, price):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO subscriptions (plan, price)
                VALUES (?, ?);
            """, (plan, price))
            self.conn.commit()
            print("Subscription inserted successfully.")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting subscription: {e}")
            return None
        
    def get_all_subscriptions(self):
        """ Retrieves all available subscription plans """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, plan, price FROM subscriptions;")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching subscriptions: {e}")
            return []

    def get_subscription_price(self, subscription_id):
        """ Retrieves the price of a specific subscription """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT price FROM subscriptions WHERE id = ?", (subscription_id,))
            price = cursor.fetchone()
            return price[0] if price else 0
        except sqlite3.Error as e:
            print(f"Error fetching subscription price: {e}")
            return 0


    def get_subscription(self, subscription_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM subscriptions WHERE id = ?;", (subscription_id,))
            subscription = cursor.fetchone()
            return subscription
        except sqlite3.Error as e:
            print(f"Error retrieving subscription: {e}")
            return None

    def update_subscription(self, subscription_id, plan=None, price=None):
        try:
            cursor = self.conn.cursor()
            fields = []
            params = []
            if plan:
                fields.append("plan = ?")
                params.append(plan)
            if price is not None:
                fields.append("price = ?")
                params.append(price)
            params.append(subscription_id)

            query = f"UPDATE subscriptions SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, params)
            self.conn.commit()
            print("Subscription updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating subscription: {e}")

    def delete_subscription(self, subscription_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM subscriptions WHERE id = ?;", (subscription_id,))
            self.conn.commit()
            print("Subscription deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting subscription: {e}")

    # ------------------------------
    # CRUD Operations for Work Rota
    # ------------------------------
    def insert_work_rota(self, staff_id, clock_in, clock_out, date):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO work_rota (staff_id, clock_in, clock_out, date)
                VALUES (?, ?, ?, ?);
            """, (staff_id, clock_in, clock_out, date))
            self.conn.commit()
            print("Work rota entry inserted successfully.")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting work rota: {e}")
            return None

    def get_work_rota(self, rota_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM work_rota WHERE id = ?;", (rota_id,))
            rota = cursor.fetchone()
            return rota
        except sqlite3.Error as e:
            print(f"Error retrieving work rota: {e}")
            return None

    # ------------------------------
    # Utility Method to Close Connection
    # ------------------------------
    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Example usage:
if __name__ == "__main__":
    # Initialise database handler
    db_handler = Database_Handler()

    # Insert a test subscription (Basic Plan)
    basic_plan_id = db_handler.insert_subscription("Basic Plan", 14.99)

    # Insert a test member (sign_up_date will be set automatically)
    member_id = db_handler.insert_member("John Doe", "john@example.com", "securepassword", basic_plan_id)

    # Fetch the inserted member to verify
    member = db_handler.get_member(member_id)
    print("Inserted member details:", member)

    # Insert an initial payment for the new member
    if member_id:
        db_handler.insert_payment(member_id, 14.99, "Credit Card", status="Paid")

    # Close the database connection after testing
    db_handler.close_connection()

