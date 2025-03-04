# Gym Management App Structure

## 1. Overview
A **Gym Management System** built using **Tkinter** for UI and **SQLite** for database handling.

---

## 2. Application Structure
### **Main Application (`Main.py`)**
Handles:
- User authentication (login/signup).
- Dashboard navigation based on role (`Admin`, `Trainer`, `Member`).
- User session management.

#### 🏠 **Session Management**
- **Session Class**: Stores `user_id`, `username`, `role`.

#### 🔑 **Authentication**
- **Login UI**
  - Fields: `Email`, `Password`
  - Buttons: `Login`, `Staff Login`, `Go to Signup`
  - Validates user credentials and redirects to respective dashboards.

- **Signup UI**
  - Fields: `Name`, `Email`, `Password`
  - Buttons: `Signup`, `Go to Login`
  - Registers a new member.

---

## 3. Dashboards & UI Components

### 📌 **User Dashboard (`UserDashboard`)**
- **Options**:
  - `Profile Management`
  - `Class Selection`
  - `Class Management`
  - `Logout`

### 📌 **Trainer Dashboard (`Trainer`)**
- **Features**:
  - View Assigned Classes.
  - Log Work Hours (Clock In/Out).
  - Track weekly work hours.

### 📌 **Admin Dashboard (`Admin`)**
- **Management Features**:
  - Manage Members
  - Manage Staff
  - Manage Classes
  - Manage Subscriptions
  - Logout

### 📌 **Class Selection (`ClassSelection`)**
- Displays **available gym classes**.
- Allows **members** to **sign up** for classes.

### 📌 **Class Management (`ClassManagement`)**
- For **Staff/Admin** to **add/edit/delete classes**.

### 📌 **Profile Management (`ProfileManagement`)**
- Allows **members** to **update** personal details.

---

## 4. Database (`database_handler.py`)

### 📦 **Tables**
- `members`: Stores member details.
- `classes`: Stores class schedules and assignments.
- `gym_staff`: Stores staff details (trainers, receptionists).
- `subscriptions`: Stores membership plans.
- `work_rota`: Tracks work hours (clock in/out).
- `admin`: Stores admin login details.

### 🔄 **Database Functions**
- **User Authentication**
  - `validate_login()`
- **Member Management**
  - `insert_member()`, `get_member()`, `update_member()`, `delete_member()`
- **Class Management**
  - `insert_class()`, `get_class()`, `update_class()`, `delete_class()`
- **Staff Management**
  - `insert_staff()`, `get_staff()`, `update_staff()`, `delete_staff()`
- **Subscription Management**
  - `insert_subscription()`, `get_subscription()`, `update_subscription()`, `delete_subscription()`
- **Work Rota (Clock In/Out)**
  - `insert_work_rota()`, `get_work_rota()`

---

## 5. Key Features & Functionalities

✅ **Login & Signup**  
✅ **Role-based Dashboards** (Admin, Trainer, Member)  
✅ **Class Registration & Management**  
✅ **Trainer Work Tracking** (Clock In/Out System)  
✅ **Subscription & Billing Handling**  
✅ **Database CRUD Operations**  

---

## 6. How to Run
1️⃣ **Install dependencies** (if needed).  
2️⃣ **Run `Main.py`** to start the application.  
3️⃣ **Login as Admin/Trainer/Member** to access respective dashboards.  

---

## 7. Future Enhancements
- 📱 **Convert into a web or mobile app**.  
- 📊 **Advanced analytics & reporting**.  
- 💳 **Integrate with payment gateways for billing**.  

---
