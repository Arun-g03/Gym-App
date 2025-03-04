import tkinter as tk
from tkinter import ttk
from database_handler import Database_Handler  # Adjust import based on your folder structure
from config import window_size



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