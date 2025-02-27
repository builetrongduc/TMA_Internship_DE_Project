import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database = db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection =create_db_connection("localhost", "root", "031103", "ecommerce_shop")

def execute_query(connection, query, values=None):
    cursor = connection.cursor()
    try:
        if values:
            if isinstance(values[0], (list, tuple)):  
                    cursor.executemany(query, values)
            else: 
                cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# Create tables
create_table_location = """
CREATE TABLE IF NOT EXISTS Location (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nation VARCHAR(100),
    City VARCHAR(100),
    District VARCHAR(100)
);
"""
#KH001, KH002, KH003
create_table_customer = """
CREATE TABLE IF NOT EXISTS Customer (
    ID VARCHAR(10) PRIMARY KEY, 
    Name VARCHAR(255) NOT NULL,
    Gender ENUM('male', 'female', 'other'),
    Age INT,
    DOB DATE,
    phoneNumber VARCHAR(20) UNIQUE,
    Address TEXT,
    locationID INT,
    FOREIGN KEY (locationID) REFERENCES Location(ID) ON DELETE SET NULL
);
"""
# SD, TK, LZD
create_table_platform = """
CREATE TABLE IF NOT EXISTS Platform (
    ID VARCHAR(10) PRIMARY KEY, 
    Platform_Name VARCHAR(100) NOT NULL,
    Platform_URL VARCHAR(500)
);
"""
# ASM, AT, AK, QJ, QS, QD, GTT, GT, GSD
create_table_category = """
CREATE TABLE IF NOT EXISTS Category (
    ID VARCHAR(10) PRIMARY KEY, 
    Name VARCHAR(255) NOT NULL,
    Type VARCHAR(100)
);
""" 

create_table_product = """
CREATE TABLE IF NOT EXISTS Product (
    ProductID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Category VARCHAR(10),
    Description TEXT,
    Brand VARCHAR(255),
    Price DECIMAL(12,2),
    Size VARCHAR(5),
    FOREIGN KEY (Category) REFERENCES Category(ID) ON DELETE SET NULL
);
"""

create_table_inventory = """
CREATE TABLE IF NOT EXISTS Inventory (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    InStock_Quantity INT NOT NULL DEFAULT 0,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);
"""

create_table_import_inventory = """
CREATE TABLE IF NOT EXISTS ImportInventory (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    ImportQuantity INT,
    Date DATE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);
"""

create_table_promotion = """
CREATE TABLE IF NOT EXISTS Promotion (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    PromoName VARCHAR(255),
    ProductID VARCHAR(20),
    Discount_rate DECIMAL(5,2),
    DateStart DATE,
    DateEnd DATE,
    PlatformID VARCHAR(10),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (PlatformID) REFERENCES Platform(ID) ON DELETE CASCADE
);
"""

create_table_applied_promotion = """
CREATE TABLE IF NOT EXISTS AppliedPromotion (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    PromotionID INT,
    CustomerID VARCHAR(10),
    FOREIGN KEY (PromotionID) REFERENCES Promotion(ID) ON DELETE CASCADE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID) ON DELETE CASCADE
);
"""
# DH0001, DH0002
create_table_order = """
CREATE TABLE IF NOT EXISTS OrderTable (
    ID VARCHAR(10) PRIMARY KEY, 
    CustomerID VARCHAR(10),
    TotalPrice DECIMAL(12,2),
    Date DATE,
    paymentMethod ENUM('cash', 'credit_card', 'momo'),
    PlatformID VARCHAR(10),
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID) ON DELETE CASCADE,
    FOREIGN KEY (PlatformID) REFERENCES Platform(ID) ON DELETE CASCADE
);
"""

create_table_order_detail = """
CREATE TABLE IF NOT EXISTS Order_Detail (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    Quantity INT,
    OrderID VARCHAR(10),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (OrderID) REFERENCES OrderTable(ID) ON DELETE CASCADE
);
"""

create_table_shipping = """
CREATE TABLE IF NOT EXISTS Shipping (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Carrier VARCHAR(255),
    OrderID VARCHAR(10),
    Status ENUM('pending', 'shipped', 'delivered', 'returned', 'cancelled') DEFAULT 'pending',
    FOREIGN KEY (OrderID) REFERENCES OrderTable(ID) ON DELETE CASCADE
);
"""

create_table_review = """
CREATE TABLE IF NOT EXISTS Review (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Review_text TEXT,
    Date DATE,
    CustomerID VARCHAR(10),
    PlatformID VARCHAR(10),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID) ON DELETE CASCADE,
    FOREIGN KEY (PlatformID) REFERENCES Platform(ID) ON DELETE CASCADE
);
"""

execute_query(connection, create_table_platform)   # Create Platform table
execute_query(connection, create_table_location)   # Create Location table
execute_query(connection, create_table_category)   # Create Category table
execute_query(connection, create_table_customer)   # Create Customer table
execute_query(connection, create_table_product)    # Create Product table
execute_query(connection, create_table_inventory)  # Create Inventory table
execute_query(connection, create_table_import_inventory)  # Create ImportInventory table
execute_query(connection, create_table_promotion)  # Create Promotion table
execute_query(connection, create_table_applied_promotion)  # Create AppliedPromotion table
execute_query(connection, create_table_order)      # Create Order table
execute_query(connection, create_table_order_detail)  # Create Order_Detail table
execute_query(connection, create_table_shipping)   # Create Shipping table
execute_query(connection, create_table_review)     # Create Review table

# Insert data into tables


# Đóng kết nối MySQL
if connection:
    connection.close()
    print("Đã đóng kết nối MySQL")