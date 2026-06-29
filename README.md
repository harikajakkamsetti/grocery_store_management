GROCERY STORE MANAGEMENT SYSTEM
(Tkinter + MySQL Project)


**Project Name**:
GroceryStoreProject



DESCRIPTION

This is a desktop-based Grocery Store Management System
developed using Python (Tkinter) and MySQL database.

It helps to manage:
- Products
- Customers
- Orders
- Billing system



PROJECT STRUCTURE


GroceryStoreProject/
|
|-- grocery_store.py              -> Main entry point of application        
|-- grocery_db.sql       -> MySQL database schema file
|
|-- images/
|     |-- img.jpeg       -> UI background image
|     |-- img2.jpg       -> UI background image
|
|-- requirements.txt     -> Python dependencies
|-- README.md            -> Project documentation



INSTALLATION & SETUP


STEP 1: Clone Repository
------------------------------------
git clone https://github.com/your-username/grocery-store-management.git
cd grocery-store-management


STEP 2: Install Dependencies
------------------------------------
pip install -r requirements.txt


STEP 3: Setup Database
------------------------------------
Open MySQL Workbench or terminal and run:

SOURCE grocery_db.sql;

OR import grocery_db.sql manually into MySQL Workbench.


STEP 4: Run Application
------------------------------------
python main.py


====================================================
DATABASE DESIGN
====================================================

DATABASE NAME:
Grocery_store


TABLES USED:


1. PRODUCTS TABLE
------------------------------------
Stores product details:

- Product_ID (Primary Key)
- Product_Name
- Units
- Price


2. ORDERS TABLE
------------------------------------
Stores order details:

- order_id (Primary Key)
- customer_name
- phone_number
- time_date
- total_cost


3. MANAGE_CUSTOMERS TABLE
------------------------------------
Stores customer additional details:

- id
- order_id (Foreign Key)
- email
- city
- age
- visits
- address
- rating


4. UNITS TABLE
------------------------------------
Stores measurement types:

- uom (Primary Key)
- uon_units (Each / Kg / Liters)


====================================================
WORKFLOW OF SYSTEM
====================================================

1. Start Application
2. Add Products into Database
3. Customer enters order details
4. Add products to cart
5. System calculates total bill automatically
6. Save order into MySQL database
7. View order history and customer details


====================================================
FEATURES
====================================================

- Add / Delete / Search Products
- Manage Inventory
- Create Customer Orders
- Auto Bill Calculation
- View Order History
- MySQL Database Integration
- Tkinter GUI Interface


====================================================
TECHNOLOGIES USED
====================================================

- Python
- Tkinter (GUI)
- MySQL Database
- Pillow (Image handling)
- mysql-connector-python


====================================================
END OF PROJECT
====================================================
