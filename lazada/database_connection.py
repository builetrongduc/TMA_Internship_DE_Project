import pandas as pd
import pymysql as pysql
import warnings
# from fake_data import fake_addata
warnings.simplefilter("ignore", UserWarning)

# Cấu hình kết nối
conn = pysql.connect(
    host="127.0.0.1",  # Địa chỉ server
    user="root",        # User
    password="",        # Mật khẩu (để trống nếu không có)
    database="qlbh",  # Thay bằng tên database
    charset="utf8mb4",  # Hỗ trợ tiếng Việt & Unicode
    cursorclass=pysql.cursors.DictCursor,
    local_infile=True
)
cursor=conn.cursor()

if conn:
    print("Kết nối thành công")


def createTables():
    create_table_location = """
    CREATE TABLE IF NOT EXISTS Location (
        ID INT PRIMARY KEY AUTO_INCREMENT,
        Nation VARCHAR(100),
        City VARCHAR(100),
        District VARCHAR(100)
    );
    """
    # KH001, KH002, KH003
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

    # Thực thi câu lệnh tạo bảng
    list_create_tables = [create_table_location, create_table_customer, create_table_platform, create_table_category, create_table_product, create_table_inventory, create_table_import_inventory, create_table_promotion, create_table_applied_promotion, create_table_order, create_table_order_detail, create_table_shipping, create_table_review]   
    for create_table in list_create_tables:
        cursor.execute(create_table)
    print("Tạo bảng thành công")

def insertCategory(cursor):
    # Thêm dữ liệu vào bảng Category với các prefix là ASM, AT, AK, QJ, QS, QD, GTT, GT, GSD với Type là thời trang nam, nữ,unisex
    insert_category = """
    INSERT INTO Category (ID, Name, Type)
    VALUES ('ASM01','Áo sơ mi', 'Nam'),
           ('AT01', 'Áo thun', 'Nam'),
           ('AK01', 'Áo khoác', 'Nam'),
           ('QJ01', 'Quần jean', 'Nam'),
           ('QS01', 'Quần short', 'Nam'),
           ('QD01', 'Quần đùi', 'Nam'),
           ('GTT01', 'Giày thể thao', 'Nam'),
           ('GT01', 'Giày tây', 'Nam'),
           ('GSD01', 'Giày sandal', 'Nam'),
           ('ASM02','Áo sơ mi', 'Nữ'),
           ('AT02', 'Áo thun', 'Nữ'),
           ('AK02', 'Áo khoác', 'Nữ'),
           ('QJ02', 'Quần jean', 'Nữ'),
           ('QS02', 'Quần short', 'Nữ'),
           ('QD02', 'Quần đùi', 'Nữ'),
           ('GTT02', 'Giày thể thao', 'Nữ'),
           ('GT02', 'Giày tây', 'Nữ'),
           ('GSD02', 'Giày sandal', 'Nữ'),
           ('ASM03','Áo sơ mi', 'Unisex'),
           ('AT03', 'Áo thun', 'Unisex'),
           ('AK03', 'Áo khoác', 'Unisex'),
           ('QJ03', 'Quần jean', 'Unisex'),
           ('QS03', 'Quần short', 'Unisex'),
           ('QD03', 'Quần đùi', 'Unisex')
    """
    cursor.execute(insert_category)
    print("Thêm dữ liệu vào bảng Product thành công")

def insertProduct(cursor):
    df=pd.read_csv('./lazada/productData/finalLazada2.csv')
    # Thêm dữ liệu vào bảng Product
    # Insert từng dòng dữ liệu của df vào bảng Product và báo log
    
    for i in range(len(df)):
        print(f"""
    INSERT INTO Product (ProductID, Name, Category, Description, Brand, Price, Size)
    VALUES ('{df['ID'][i]}', '{df['name'][i]}', '{df['category'][i]}', '{df['description'][i]}', '{df['brand_name'][i]}', {df['price'][i]}, '{df['size'][i]}')
    """)
        cursor.execute(f"""
    INSERT INTO Product (ProductID, Name, Category, Description, Brand, Price, Size)
    VALUES ('{df['ID'][i]}', '{df['name'][i]}', '{df['category'][i]}', '{df['description'][i]}', '{df['brand_name'][i]}', {df['price'][i]}, '{df['size'][i]}')
    """)
        print('DONE',i)

def insertPlatform(cursor):
    # Thêm dữ liệu vào bảng Platform với các prefix là SD, TK, LZD
    insert_platform = """
    INSERT INTO Platform (ID, Platform_Name, Platform_URL)
    VALUES ('SENDO', 'Sendo', 'https://www.sendo.vn/'),
         ('TIKI', 'Tiki', 'https://tiki.vn/'),
         ('LAZADA', 'Lazada', 'https://www.lazada.vn/')
    """
    cursor.execute(insert_platform)
    print("Thêm dữ liệu vào bảng Platform thành công")

# Fake for Review Table
import random
from faker import Faker

fake=Faker()


def fakeRating():
    rows_products=cursor.execute(f"SELECT * FROM product;")
    rows_products=cursor.fetchall()
    df=pd.DataFrame(rows_products)
    row_customers=cursor.execute(f"SELECT * FROM customer;")
    row_customers=cursor.fetchall()
    df_customers=pd.DataFrame(row_customers)
    df_productinfo=df[['ProductID','Name']]
    list_productid=df_productinfo['ProductID'].tolist()
    list_customeid=df_customers['ID'].tolist()
    list_review=[]
    for _ in range(100):
        product_id=random.choice(list_productid)
        df_name = df_productinfo[df_productinfo["ProductID"] == product_id]
        # name_product=df_name['Name'].values[0]
        rating=random.randint(1,5)
        date=fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d")
        customer_id=random.choice(list_customeid)
        platform_id=random.choice(['SENDO','TIKI','LAZADA'])
        if rating >=4:
            opinion='rất tốt. Tôi khá hài lòng với sản phẩm này'
        elif rating >=3 and rating <4:
            opinion='cũng tạm. Cần cải thiện hơn'
        else:
            opinion='không tốt. Tôi không hài lòng với sản phẩm này'
        review_text=f'Sản phẩm này {opinion}'
        review_info={
            "product_id":product_id,
            "rating":rating,
            "review_text":review_text,
            'date':date,
            'customer_id':customer_id,
            'platform_id':platform_id
        }
        list_review.append(review_info)
    
    # transform list review to dataframe
    df_review=pd.DataFrame(list_review)
    df_review.to_csv('reviewData.csv',index=False,encoding='utf-8')
    
    for review in list_review:
        cursor.execute(f"""
        INSERT INTO Review (ProductID, Rating, Review_text, Date, CustomerID, PlatformID)
        VALUES ('{review['product_id']}', {review['rating']}, '{review['review_text']}', '{review['date']}', '{review['customer_id']}', '{review['platform_id']}')
        """)
        print('DONE')



# insertPlatform(cursor)
fakeRating()

conn.commit()
cursor.close()
conn.close()
print('Disconnected')
