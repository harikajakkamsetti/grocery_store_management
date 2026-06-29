import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime


# Database configuration
_config = {
    'user': 'root',
    'password': '99890',
    'host': '127.0.0.1',
    'database': 'Grocery_store',
    'raise_on_warnings': True
}

class GroceryStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Store Management")
        self.current_page = None

        # Load the background image
        self.image = Image.open("C:\\Users\\harik\\OneDrive\\Desktop\\grocery store mangementp\\images\\img2.jpg")
        self.image = self.image.resize((1600, 1200))
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label with the image
        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack(fill="both", expand=True)

        # Keep a reference to the image to prevent it from being garbage collected
        self.label.image = self.photo

        # Create a heading label
        heading_label = tk.Label(self.root, text="Welcome to Grocery Store", font=("Helvetica", 38, "bold"), fg="white", bg="red", padx=10, pady=20, relief="raised", bd=5)
        heading_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Create a start button
        start_button = tk.Button(self.root, text="START", width=12, height=2, font=("Arial", 15, "bold"), fg="black", bg="#33FF33", relief="ridge", bd=5, command=self.open_management_page)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a label below the start button
        fresh_vibes_label = tk.Label(self.root, text="Fresh vibes only!!", font=("Arial", 18, "bold"), fg="#FF007F")
        fresh_vibes_label.place(relx=0.5, rely=0.6, anchor=tk.W)

    def open_management_page(self):
        self.root.state('zoomed')  # Maximize the window
        self.clear_page()
        self.current_page = ManagementPage(self.root, self.open_new_order_page, self.open_manage_product_page)

    def open_new_order_page(self):
        self.clear_page()
        NewOrderPage(self.root, self.open_management_page)

    def open_manage_product_page(self):
        self.clear_page()
        ManageProductPage(self.root, self.open_management_page)

    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class ManagementPage:
    def __init__(self, master, new_order_callback, manage_product_callback):
        self.master = master
        self.new_order_callback = new_order_callback
        self.manage_product_callback = manage_product_callback

        # Load the background image
        self.image = Image.open("C:\\Users\\harik\\OneDrive\\Desktop\\grocery store mangementp\\images\\img.jpeg")
        self.photo = ImageTk.PhotoImage(self.image)
        background_label = tk.Label(self.master, image=self.photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to the image to prevent it from being garbage collected
        background_label.image = self.photo

        # Heading label for management page
        heading_label = ttk.Label(self.master, text="Grocery Store Management System", font=("Arial", 24, "bold"))
        heading_label.pack(pady=20)

        # Create a frame for the buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        # Create the buttons
        manage_products_button = tk.Button(button_frame, text="Manage Products", font=("Arial", 13, "bold"), command=self.manage_product_callback, bg="red", fg="black")
        manage_products_button.pack(side="left", padx=2)

        new_order_button = tk.Button(button_frame, text="New Order", font=("Arial", 13, "bold"), command=self.new_order_callback, bg="red", fg="black")
        new_order_button.pack(side="left", padx=2)

        # Create a frame for the table
        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(pady=20)

        # Create the table
        self.my_first_table_db = ttk.Treeview(self.table_frame, height=22, show='headings')
        self.my_first_table_db['columns'] = ['CUSTOMER NAME', 'ORDER ID', 'TIME & DATE', 'TOTAL COST', 'PHONE NUMBER']

        # Define column properties
        for col in self.my_first_table_db['columns']:
            self.my_first_table_db.heading(col, text=col, anchor=tk.W)
            self.my_first_table_db.column(col, anchor=tk.W, width=250)

        # Configure column heading font
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 10))

        self.my_first_table_db.pack()

        # Connect to the database and fetch orders
        self.connect_to_database()
        self.fetch_orders()

        # Create a close button
        close_button = tk.Button(self.master, text="Close", width=10, height=1, font=("Arial", 15, "bold"), fg ="black", bg="red", relief="ridge", bd=5, command=self.master.destroy)
        close_button.pack(pady=10)

    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(**_config)
            if self.conn.is_connected():
                print('Database connected')
        except mysql.connector.Error as err:
            print(err)

    def fetch_orders(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM grocery_store.orders;")
        resultado = cur.fetchall()

        for index, row in enumerate(resultado):  # Use enumerate to get both index and row
            # Insert the order into the Treeview
            if index % 2 == 0:
                self.my_first_table_db.insert('', 'end', values=row, tags=('evenrow',))
            else:
                self.my_first_table_db.insert('', 'end', values=row, tags=('oddrow',))

        # Configure row styles
        self.my_first_table_db.tag_configure('evenrow', background='#ffcccc', font=("Arial", 12))  # Light gray for even rows
        self.my_first_table_db.tag_configure('oddrow', background='white', font=("Arial", 12))      # White for odd rows

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.my_first_table_db.yview)
        self.my_first_table_db.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        self.my_first_table_db.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind the double-click event to the Treeview
        self.my_first_table_db.bind("<Double-1>", self.on_row_double_click)
        
        
        

    def on_row_double_click(self, event):
        # Get the selected item
        selected_item = self.my_first_table_db.selection()[0]
        # Get the values of the selected item
        order_details = self.my_first_table_db.item(selected_item, 'values')
        # Call the method to view order details
        self.view_order_details(order_details)

    def view_order_details(self, order):
        # This function will show the details of the order in a new window
        details_window = tk.Toplevel(self.master)
        details_window.title("Order Details")

        # Display order details
        tk.Label(details_window, text=f"Order ID: {order[1]}").pack(pady=5)
        tk.Label(details_window, text=f"Customer Name: {order[0]}").pack(pady=5)
        tk.Label(details_window, text=f"Total Cost : {order[3]}").pack(pady=5)
        tk.Label(details_window, text=f"Phone Number: {order[4]}").pack(pady=5)
    def view_order_details(self, order):
    # This function will show the details of the order in a new window
        details_window = tk.Toplevel(self.master)
        details_window.title("Order Details")

        # Display order details
        tk.Label(details_window, text=f"Order ID: {order[1]}",font=("Arial", 12,"bold")).pack(pady=5)
        tk.Label(details_window, text=f"Customer Name: {order[0]}",font=("Arial", 12,"bold")).pack(pady=5)
        tk.Label(details_window, text=f"Total Cost: {order[3]}",font=("Arial", 12)).pack(pady=5)
        tk.Label(details_window, text=f"Phone Number: {order[4]}",font=("Arial", 12,"bold")).pack(pady=5)

        # Fetch customer data from manage_customers table based on order ID
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM grocery_store.manage_customers WHERE order_id = %s", (order[1],))
        customer_data = cur.fetchone()

        # Check if customer data exists
        if customer_data:
            # Assuming customer_data has columns: order_id, address, email, etc.
            tk.Label(details_window, text=f"Customer city: {customer_data[1]}",font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"Customer Email: {customer_data[0]}",font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"age: {customer_data[3]}",font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"No.of.times visited: {customer_data[4]}",font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"current address: {customer_data[5]}",font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"rating: {customer_data[6]}",font=("Arial", 12,"bold")).pack(pady=5)
            # Add more labels for other customer data columns as needed
        else:
            tk.Label(details_window, text="No customer data found for this order ID.").pack(pady=5)

class NewOrderPage:
    def __init__(self, master, back_callback):
        self.master = master
        self.back_callback = back_callback  # Store the back callback
        self.create_order_page()

    def create_order_page(self):
        # Clear existing widgets if any
        for widget in self.master.winfo_children():
            widget.destroy()

        self.image = Image.open("C:\\Users\\harik\\OneDrive\\Desktop\\grocery store mangementp\\images\\img.jpeg")
        self.photo = ImageTk.PhotoImage(self.image)
        background_label = tk.Label(self.master, image=self.photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to the image to prevent it from being garbage collected
        background_label.image = self.photo

        # Database connection
        self.conn = None
        self.connect_to_database()

        # Customer Information Frame
        customer_frame = tk.Frame(self.master)
        customer_frame.pack(pady=10, padx=10, anchor='nw')

        # Customer Name Entry
        tk.Label(customer_frame, text="Customer Name:", font=("Times New Roman", 13, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.customer_name_entry = tk.Entry(customer_frame, width=25, font=("Times New Roman", 15))
        self.customer_name_entry.pack(side=tk.LEFT)

        # Phone Number Entry
        tk.Label(customer_frame, text="Phone Number:", font=("Times New Roman", 13, "bold")).pack(side=tk.LEFT, padx=(10, 5))
        self.phone_number_entry = tk.Entry(customer_frame, width=15, font=("Times New Roman", 15))
        self.phone_number_entry.pack(side=tk.LEFT)

        # Submit Button
        tk.Button(customer_frame, text="Submit", font=("Times New Roman", 13), command=self.submit_customer_info, bg="red").pack(side=tk.LEFT, padx=(5, 0))

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))  # Set font size to 12 for Treeview items

        # Create Treeview for Products
        self.tree = ttk.Treeview(self.master, columns=("Product", "Price", "Quantity", "Total"), show="headings")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total", text="Total")
        self.tree.pack(padx=250, pady=50,fill=tk.BOTH, expand=True)

        customer_frame2 = tk.Frame(self.master)
        customer_frame2.pack(pady=10, padx=10)

        # Entry field for Product ID
        tk.Label(customer_frame2, text="Product ID:",font=("Arial", 12,"bold")).pack(padx=10, pady=10,side=tk.LEFT)
        self.product_id_entry = tk.Entry(customer_frame2, font=("Times New Roman", 15,"bold"))
        self.product_id_entry.pack(padx=10, pady=10,side=tk.LEFT)
        self.product_id_entry.bind("<Return>", self.get_product_details)  # Bind Enter key to fetch product details

        # Entry fields for product name, price, and quantity
        tk.Label(customer_frame2, text="Product Name:",font=("Arial", 12,"bold")).pack(padx=10, pady=10,side=tk.LEFT)
        self.product_name_entry = tk.Entry( customer_frame2, font=("Times New Roman", 15, "bold"), state='readonly')
        self.product_name_entry.pack(padx=10, pady=10,side=tk.LEFT)

        tk.Label(customer_frame2, text="Price:",font=("Arial", 12,"bold")).pack(padx=10, pady=10,side=tk.LEFT)
        self.price_entry = tk.Entry(customer_frame2, font=("Times New Roman", 15, "bold"), state='readonly')
        self.price_entry.pack(padx =10, pady=10,side=tk.RIGHT)

        tk.Label(self.master, text="Quantity:",font=("Arial", 12,"bold")).pack(padx=10, pady=10)
        self.quantity_entry = tk.Entry(self.master, font=("Times New Roman", 15 ,"bold"))
        self.quantity_entry.pack(padx=10, pady=10)

        customer_frame1 = tk.Frame(self.master)
        customer_frame1.pack(pady=10, padx=10)

        # Create buttons for adding, removing, and saving order
        tk.Button(customer_frame1, text="Add Item", font=("Times New Roman", 15), command=self.add_item, bg="red").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(customer_frame1, text="Remove Item", font=("Times New Roman", 15), command=self.remove_item, bg="red").pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Button(self.master, text="Save Order", font=("Times New Roman", 16), command=self.save_order, fg="white", bg="green").pack(padx=10, pady=10)

        # Back Button
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10, padx=10, side=tk.TOP, anchor='ne')
        tk.Button(button_frame, text="Back", font=("Times New Roman", 18), command=self.back_callback, bg="red").pack(side=tk.TOP)

    def connect_to_database(self):
        _config = {
            'user': 'root',  # Removed the trailing space
            'password': '99890',
            'host': '127.0.0.1',
            'database': 'Grocery_store',
            'raise_on_warnings': True
        }

        try:
            self.conn = mysql.connector.connect(**_config)
            if self.conn.is_connected():
                print('Database connected')
        except mysql.connector.Error as err:
            print(err)
            messagebox.showerror("Error", "Database connection failed.")
            self.conn = None

    def get_product_details(self, event):
        if self.conn is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        product_id = self.product_id_entry.get()
        if not product_id.isdigit():
            messagebox.showerror("Error", "Product ID must be a number.")
            return

        cur = self.conn.cursor()
        cur.execute("SELECT product_name, price FROM products WHERE product_id = %s", (product_id,))
        product_details = cur.fetchone()
        if product_details:
            self.product_name_entry.config(state='normal')
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.insert(0, product_details[0])
            self.product_name_entry.config(state='readonly')

            self.price_entry.config(state='normal')
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, product_details[1])
            self.price_entry.config(state='readonly')
        else:
            messagebox.showerror("Error", "Product not found.")

    def add_item(self):
        if self.conn is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        product_name = self.product_name_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        # Check if inputs are valid
        if not product_name:
            messagebox.showerror("Error", "Please enter a product ID.")
            return
        if not price.isdigit():
            messagebox.showerror("Error", "Price must be a number.")
            return
        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        # Calculate total
        total = int(price) * int(quantity)

        # Insert item into treeview
        self.tree.insert("", tk.END, values=(product_name, price, quantity, total))

        # Clear entry fields
        self.product_id_entry.delete(0, tk.END)
        self.product_name_entry.config(state='normal')
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.config(state='readonly')
        self.price_entry.config(state='normal')
        self.price_entry.delete(0, tk.END)
        self.price_entry.config(state='readonly')
        self.quantity_entry.delete(0, tk.END)

    def remove_item(self):
        if self.conn is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)

    def save_order(self):
        if self.conn is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        customer_name = self.customer_name_entry.get()
        phone_number = self.phone_number_entry.get()

        if not customer_name:
            messagebox.showerror("Error", "Please enter a customer name.")
            return
        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number.")
            return

        # Calculate total cost
        total_cost = 0
        for item in self.tree.get_children():
            total_cost += int(self.tree.item(item, 'values')[3])

        # Generate bill
        bill_text = f"Customer Name: {customer_name}\nPhone Number: {phone_number}\n\n"
        for item in self.tree.get_children():
            product = self.tree.item(item, 'values')[0]
            price = self.tree.item(item, 'values')[1]
            quantity = self.tree.item(item, 'values')[2]
            total = self.tree.item(item, 'values')[3]
            bill_text += f"\nProduct: {product}, Price: {price}, Quantity: {quantity}, Total: {total}\n"
        bill_text += f"\n**Total Cost: {total_cost}**"


        # Save order to database
        try:
            cur = self.conn.cursor()
            query = "INSERT INTO orders (customer_name, phone_number, time_date, total_cost) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (customer_name, phone_number, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_cost))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to save order: {err}")
        finally:
            cur.close()  # Ensure the cursor is closed

        # Clear treeview and entry fields
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.customer_name_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)

        # Switch to bill page
        self.create_bill_page(bill_text)

    def create_bill_page(self, bill_text):
        # Clear existing widgets if any
        for widget in self.master.winfo_children():
            widget.destroy()

        # Create a new frame for the bill page
        bill_frame = tk.Frame(self.master)
        bill_frame.pack(pady=10, padx=10)

        # Display the bill text
        tk.Label(bill_frame, text=bill_text, font=("Arial", 12), wraplength=400).pack(padx=10, pady=10)

        # Create buttons for printing the bill and going back
        button_frame = tk.Frame(bill_frame)
        button_frame.pack(pady=10, padx=10)

        tk.Button(button_frame, text="Print Bill", font=("Times New Roman", 15), command=lambda: messagebox.showinfo("Success", "Bill printed successfully."), bg="red").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="Back", font=("Times New Roman", 15), command=self.create_order_page, bg="red").pack(side=tk.RIGHT, padx=10, pady=10)

    def submit_customer_info(self):
        customer_name = self.customer_name_entry.get()
        phone_number = self.phone_number_entry.get()

        if not customer_name:
            messagebox.showerror("Error", "Please enter a customer name.")
            return
        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number.")
            return

        # Perform any additional actions or validation here
        messagebox.showinfo("Success", "Customer information submitted successfully.")

class ManageProductPage:
    def __init__(self, master, back_callback):
        self.master = master
        self.image = Image.open("C:\\Users\\harik\\OneDrive\\Desktop\\grocery store mangementp\\images\\img.jpeg")
        self.photo = ImageTk.PhotoImage(self.image)
        background_label = tk.Label(self.master, image=self.photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to the image to prevent it from being garbage collected
        background_label.image = self.photo

        heading_label = ttk.Label(self.master, text="Manage Products", font=("Arial", 28, "bold"))
        heading_label.pack(pady=20)

        # Database connection
        self.connect_to_database()

        # Create a frame for the search bar
        search_frame = tk.Frame(self.master)
        search_frame.pack(pady=10)

        # Create the search entry
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.bind('<Return>', lambda event: self.search_products())       
        self.search_entry.pack(side="left", padx=5)
        

        # Create the search button
        search_button = tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), command=self.search_products, bg="red", fg="black")
        search_button.pack(side="right")

        # Create a frame for the table
        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(pady=20, padx=20)

        # Create the table
        self.my_first_table_db = ttk.Treeview(self.table_frame, height=24, show='headings')
        self.my_first_table_db['columns'] = ('Product ID', 'Product Name', 'Units', 'Price', 'Measurement')

        # Define column properties with increased font size and bold style
        for col in self.my_first_table_db['columns']:
            self.my_first_table_db.heading(col, text=col, anchor=tk.W)
            self.my_first_table_db.column(col, anchor=tk.W, width=250)

        # Configure column heading font
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        self.my_first_table_db.pack(side=tk.LEFT)
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.my_first_table_db.yview)
        self.my_first_table_db.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Connect to the database and fetch products after the table is created
        self.fetch_products()

        # Create a frame for the buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        # Create the buttons
        add_product_button = tk.Button(button_frame, text="Add Product", font=("Arial", 13, "bold"), command=self.add_product, bg="red", fg="black")
        add_product_button.pack(side="left", padx=2)

        # Create a back button
        back_button = tk.Button(button_frame, text="Back", font=("Arial", 13, "bold"), command=back_callback, bg="red")
        back_button.pack(side="left", padx=2)

        # Bind double-click event to delete product
        self.my_first_table_db.bind("<Double-1>", self.confirm_delete_product)

        # Bind right-click event to show product details
        self.my_first_table_db.bind("<Button-3>", self.show_product_details)

        # Configure row styles for highlighting
        self.my_first_table_db.tag_configure('highlight', background='lightblue')

    def connect_to_database(self):
        _config = {
            'user': 'root',
            'password': '99890',
            'host': '127.0.0.1',
            'database': 'Grocery_store',
            'raise_on_warnings': True
        }

        try:
            self.conn = mysql.connector.connect(**_config)
            if self.conn.is_connected():
                print('Database connected')
        except mysql.connector.Error as err:
            print(err)

    def fetch_products(self):
        cur = self.conn.cursor()
        cur.execute("SELECT products.Product_ID, products.Product_Name, products.Units, products.Price, units.uon_units FROM products INNER JOIN units ON products.Units=units.uom;")
        resultado = cur.fetchall()

        for row in resultado:
            self.my_first_table_db.insert('', 'end', values=row)

    def add_product(self):
        # Create a new window to input product information
        product_window = tk.Toplevel(self.master)
        product_window.title("Add Product")

        # Create labels and entries for product name, unit, and price
        tk.Label(product_window, text="Product Name:").grid(row=0, column=0, padx=10, pady=10)
        product_name_entry = tk.Entry(product_window)
        product_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(product_window, text=" Units:\n1.each\n 2.kg\n3.liters").grid(row=1, column=0, padx=10, pady=10)
        unit_entry = tk.Entry(product_window)
        unit_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(product_window, text="Price:").grid(row=2, column=0, padx=10, pady=10)
        price_entry = tk.Entry(product_window)
        price_entry.grid(row=2, column=1, padx=10, pady=10)

        def submit_product():
            product_name = product_name_entry.get()
            Units = unit_entry.get()
            price = price_entry.get()

            # Validate input
            if not product_name or not Units or not price:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            # Insert product information into the database
            query = "INSERT INTO products (product_name, Units, price) VALUES (%s, %s, %s)"
            cur = self.conn.cursor()
            cur.execute(query, (product_name, Units, price))
            self.conn.commit()

            # Display product information
            messagebox.showinfo("Product Information", f"Product Name: {product_name}\nUnit: {Units}\nPrice: {price}\nadded successfully!!")

            # Refresh the product table
            self.my_first_table_db.delete(*self.my_first_table_db.get_children())
            self.fetch_products()

            # Close the product window
            product_window.destroy()

        submit_button = tk.Button(product_window, text="Submit", bg="green", font=("Arial", 13, "bold"), command=submit_product)
        submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def confirm_delete_product(self, event):
        selected_item = self.my_first_table_db.selection()[0]
        product_id = self.my_first_table_db.item(selected_item, 'values')[0]

        # Prompt for deletion confirmation
        if messagebox.askyesno("Delete Product", f"Are you sure you want to delete product with ID {product_id}?"):
            # Delete product from database
            query = "DELETE FROM products WHERE Product_ID = %s"
            cur = self.conn.cursor()
            cur.execute(query, (product_id,))
            self.conn.commit()

            # Refresh the product table
            self.my_first_table_db.delete(*self.my_first_table_db.get_children())
            self.fetch_products()

    def show_product_details(self, event):
        details_window = tk.Toplevel(self.master)
        details_window.title("Product Details")
        # Get the selected item
        selected_item = self.my_first_table_db.identify_row(event.y)
        if selected_item:
            product_id = self.my_first_table_db.item(selected_item, 'values')[0]

            # Fetch product details from manage_orders table
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM manage_orders WHERE product_id = %s", (product_id,))
            product_details = cur.fetchone()

            if product_details:
                # Display product details in a message box
                tk.Label(details_window, text=f"product id: {product_id[0]}",font=("Arial", 12)).pack(pady=5)
                tk.Label(details_window, text=f"SELLING COMAPANY: {product_details[1]}",font=("Arial", 12)).pack(pady=5)
                tk.Label(details_window, text=f"DATE OF PURCHASING: {product_details[2]}",font=("Arial", 12)).pack(pady=5)
                tk.Label(details_window, text=f"EXISTED STOCK: {product_details[3]}",font=("Arial", 12)).pack(pady=5)
                tk.Label(details_window, text=f"EXPIED DATE: {product_details[4]}",font=("Arial", 12)).pack(pady=5)
            # Add more labels for other customer data columns as needed
            else:
                tk.Label(details_window, text="No data found for this product ID.",font=("Arial",  12)).pack(pady=5)

    def search_products(self):
        search_query = self.search_entry.get().strip()  # Get the search query and remove any leading/trailing whitespace
        self.my_first_table_db.delete(*self.my_first_table_db.get_children())  # Clear the table

        cur = self.conn.cursor()

        if not search_query:
            # If the search query is empty, fetch all products
            cur.execute("""
                SELECT products.Product_ID, products.Product_Name, products.Units, products.Price, units.uon_units 
                FROM products 
                INNER JOIN units ON products.Units=units.uom
            """)
        else:
            # Execute the search query
            cur.execute("""
                SELECT products.Product_ID, products.Product_Name, products.Units, products.Price, units.uon_units 
                FROM products 
                INNER JOIN units ON products.Units=units.uom 
                WHERE products.Product_Name LIKE %s OR products.Product_ID LIKE %s
            """, ('%' + search_query + '%', '%' + search_query + '%'))

        resultado = cur.fetchall()

        # Check if any results were found
        if not resultado and search_query:
            messagebox.showinfo("Search Result", "No matching products found.")
            return

        # Insert results into the table
        for row in resultado:
            self.my_first_table_db.insert('', 'end', values=row)

        # Optionally, you can set the focus to the first item in the results
        if resultado:
            self.my_first_table_db.selection_set(self.my_first_table_db.get_children()[0])
if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryStoreApp(root)
    root.mainloop()
