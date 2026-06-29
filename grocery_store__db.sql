-- =========================================
-- DATABASE CREATION
-- =========================================
CREATE DATABASE IF NOT EXISTS Grocery_store;
USE Grocery_store;

-- =========================================
-- UNITS TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS units (
    uom INT PRIMARY KEY,
    uon_units VARCHAR(50)
);

INSERT INTO units (uom, uon_units) VALUES
(1, 'Each'),
(2, 'Kg'),
(3, 'Liters');

-- =========================================
-- PRODUCTS TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS products (
    Product_ID INT AUTO_INCREMENT PRIMARY KEY,
    Product_Name VARCHAR(100) NOT NULL,
    Units INT,
    Price DECIMAL(10,2),
    FOREIGN KEY (Units) REFERENCES units(uom)
);

-- =========================================
-- ORDERS TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    phone_number VARCHAR(20),
    time_date DATETIME,
    total_cost DECIMAL(10,2)
);

-- =========================================
-- CUSTOMER DETAILS TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS manage_customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    email VARCHAR(100),
    city VARCHAR(100),
    age INT,
    visits INT,
    address VARCHAR(255),
    rating INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- =========================================
-- SAMPLE DATA (optional)
-- =========================================
INSERT INTO products (Product_Name, Units, Price) VALUES
('Rice', 2, 60),
('Milk', 3, 50),
('Soap', 1, 20);