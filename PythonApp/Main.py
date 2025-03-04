import tkinter as tk
from database_handler import Database_Handler
from config import window_size
from Login import LoginUI

def initialise_database():
    """ Ensures the database tables are created before the app starts. """
    db_handler = Database_Handler()
    db_handler.create_tables()

def main():
    """ Main function to initialise the gym management application. """
    initialise_database()  # Set up database tables

    root = tk.Tk()
    root.geometry(window_size)
    root.title("World Gym Management System")
    
    login_ui = LoginUI(root)  # Start with the Login screen
    root.mainloop()

if __name__ == "__main__":
    main()
