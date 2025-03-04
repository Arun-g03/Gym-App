# Gym Management System (Using SQLite & Tkinter)

## Project Structure

gym_management_app/ 
├── database/ │ 
├── db_setup.py (Handles SQLite database creation and table setup) │ 
├── db_operations.py (Handles CRUD operations for users, classes, subscriptions, trainers, etc.) │ 
├── ui/ │ ├── main.py (Main entry point, Tkinter UI setup, navigation between screens) │ 
├── login.py (Login/Register screen UI and authentication logic) │ 
├── dashboard.py (Main user dashboard after login - menu for other features) │ 
├── member_management.py (UI for member profile & subscription tracking) │ 
├── class_scheduling.py (UI for gym class scheduling, sign-ups, etc.) │ 
├── trainer_assignment.py (UI for assigning trainers & tracking work hours) │ 
├── models/ │ ├── member.py (Class handling member attributes & subscription details) │ 
├── trainer.py (Class handling trainer attributes & work hour tracking) │ 
├── class.py (Class handling gym classes & scheduling info) │ 
├── tests/ │ 
├── test_database.py (Unit tests for database CRUD operations) │ 
├── test_ui.py (Basic UI functionality tests using Tkinter Test tools) │ 
├── requirements.txt (Dependencies, if any) 
├── README.md (Project overview & setup instructions)