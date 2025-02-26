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

connection =create_db_connection("localhost", "root", "031103", "ecommerce_db")

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
create_table_platform = """
CREATE TABLE Platform (
    ID VARCHAR(5) PRIMARY KEY,
    Platform_Name VARCHAR(50) NOT NULL,
    Platform_URL VARCHAR(500)
);
"""
create_table_category = """
CREATE TABLE Category (
    ID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Path VARCHAR(255),
    PlatformID VARCHAR(5),
    FOREIGN KEY (PlatformID) REFERENCES Platform(ID)
);
"""
create_table_seller = """
CREATE TABLE Seller (
    SellerID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Link VARCHAR(500),
    Location VARCHAR(255),
    Rating FLOAT,
    Type VARCHAR(100)
);
"""
create_table_location = """
CREATE TABLE Location (
    ID VARCHAR(5) PRIMARY KEY,
    Nation VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL
);
"""
create_table_product = """
CREATE TABLE Product (
    ProductID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Category VARCHAR(20),
    Description TEXT,
    Brand VARCHAR(255),
    Num_sold INT,
    Rating FLOAT,
    Num_rate INT,
    Seller VARCHAR(20),
    PlatformID VARCHAR(5),
    URLProduct VARCHAR(500),
    OriginalPrice DECIMAL(12,2),
    URLImage VARCHAR(500),
    FOREIGN KEY (Category) REFERENCES Category(ID),
    FOREIGN KEY (Seller) REFERENCES Seller(SellerID),
    FOREIGN KEY (PlatformID) REFERENCES Platform(ID)
);
"""
create_table_review = """
CREATE TABLE Review (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    Rating INT,
    Review_text TEXT,
    Date DATE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
"""
create_table_history_inventory = """
CREATE TABLE History_Inventory (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    InStock_Quantity INT,
    Date DATE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
"""
create_table_history_price = """
CREATE TABLE History_Price (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    Price DECIMAL(10,2),
    Date DATE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
"""
create_table_promotion = """
CREATE TABLE Promotion (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID VARCHAR(20),
    Discount_rate FLOAT,
    Date DATE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
"""
execute_query(connection, create_table_platform)   # Create Platform table
execute_query(connection, create_table_category)   # Create Category table
execute_query(connection, create_table_seller)     # Create Seller table
execute_query(connection, create_table_location)   # Create Location table
execute_query(connection, create_table_product)    # Create Product table
execute_query(connection, create_table_review)     # Create Review table
execute_query(connection, create_table_history_inventory) # Create History_Inventory table
execute_query(connection, create_table_history_price)     # Create History_Price table
execute_query(connection, create_table_promotion)        # Create Promotion table

# Insert data into tables


# Đóng kết nối MySQL
if connection:
    connection.close()
    print("Đã đóng kết nối MySQL")
