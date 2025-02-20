from selenium import webdriver
import time
from bs4 import BeautifulSoup


# Khởi tạo trình duyệt
driver = webdriver.Edge('')
product_data_lazada=[]
product_data_sendo=[]
product_data_tiki=[]


# Crawl từ trang 1 đến trang 3
def crawl_lazada(page_number,product_data,keyword):
    for page in range(1, page_number):
        print(f"🔄 Đang lấy dữ liệu từ trang {page}...")

        # Tạo URL của trang Lazada
        url = f"https://www.lazada.vn/tag/{keyword}/?catalog_redirect_tag=true&page={page}&q={keyword}&spm=a2o4n.homepage.search.d_go"
        
        # Mở trang
        driver.get(url)
        time.sleep(5)  # Chờ trang load

        # Lấy source code đã render
        page_source = driver.page_source

        # Parse HTML với BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Tìm tất cả sản phẩm
        products = soup.find_all("div", class_="buTCk")

        for product in products:
            # Lấy thẻ <a> chứa thông tin sản phẩm
            a_tag = product.find("a")
            title = a_tag.get("title", "").strip() if a_tag else "Không có tiêu đề"
            link = "https:" + a_tag.get("href", "").strip() if a_tag else "Không có link"

            # Lấy giá sản phẩm
            price_tag = product.find("div", class_="aBrP0")
            price = price_tag.find("span", class_="ooOxS").text.strip() if price_tag else "Không có giá"

            # Lấy số lượng đã bán
            sold_tag = product.find("span", class_="_1cEkb")
            sold = sold_tag.text.strip() if sold_tag else "Không có thông tin bán"

            # Lấy số đánh giá
            rating_tag = product.find("span", class_="qzqFw")
            rating = rating_tag.text.strip("()") if rating_tag else "0"

            # Lấy xuất xứ
            location_tag = product.find("span", class_="oa6ri")
            location = location_tag.text.strip() if location_tag else "Không có thông tin"

            # Thêm dữ liệu vào danh sách
            product_data.append((title, price, sold, rating, location, link))

def crawl_sendo(page_number,product_data,keyword):
    for page in range(1, page_number):
        print(f"🔄 Đang lấy dữ liệu từ trang {page}...")
        url=f"https://www.sendo.vn/tim-kiem?q={keyword}&p={page}"
        # Mở trang
        driver.get(url)
        time.sleep(5)  # Chờ trang load

        # Lấy source code đã render
        page_source = driver.page_source

        # Parse HTML với BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")


        # Tìm tất cả sản phẩm trên trang
        products = soup.find_all("div", class_="d7ed-d4keTB")


        for product in products:
            # Lấy thẻ <a> chứa link & tên sản phẩm
            a_tag = product.find("a")
            title = a_tag.text.strip() if a_tag else "Không có tiêu đề"
            link = a_tag.get("href", "").strip() if a_tag else "Không có link"
            link = "https://www.sendo.vn" + link if link.startswith("/") else link

            # Lấy giá gốc (trước giảm giá)
            original_price_tag = product.find("span", class_="d7ed-bm83Kw")
            original_price = original_price_tag.text.strip() if original_price_tag else "Không có giá gốc"

            # Lấy giá khuyến mãi
            discount_price_tag = product.find("span", class_="d7ed-CLUDGW")
            discount_price = discount_price_tag.text.strip() if discount_price_tag else "Không có giá khuyến mãi"

            # Lấy phần trăm giảm giá
            discount_percent_tag = product.find("span", class_="d7ed-UPrmtp")
            discount_percent = discount_percent_tag.text.strip() if discount_percent_tag else "Không có giảm giá"

            # Lấy xuất xứ (tỉnh thành)
            location_tag = product.find("span", class_="d7ed-mzOLVa")
            location = location_tag.text.strip() if location_tag else "Không có thông tin"

            # Thêm dữ liệu vào danh sách
            product_data.append((title, original_price, discount_price, discount_percent, location, link))

def crawl_tiki(page_number,product_data,keyword):
    for page in range(1, page_number):
        print(f"🔄 Đang lấy dữ liệu từ trang {page}...")
        url=f"https://tiki.vn/search?q={keyword}&page={page}"
        # Mở trang
        driver.get(url)
        time.sleep(5)  # Chờ trang load

        # Lấy source code đã render
        page_source = driver.page_source

        # Parse HTML với BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Tìm tất cả sản phẩm trên trang
        products = soup.find_all("div", class_="styles__ProductItemContainerStyled-sc-bszvl7-0")

        for product in products:
            # Lấy thẻ <a> chứa link & tên sản phẩm
            a_tag = product.find("a", class_="style__ProductLink-sc-139nb47-2")
            title = a_tag.find("h3").text.strip() if a_tag else "Không có tiêu đề"
            link = "https://tiki.vn" + a_tag.get("href", "").strip() if a_tag else "Không có link"

            # Lấy giá sản phẩm
            price_tag = product.find("div", class_="price-discount__price")
            price = price_tag.text.strip() if price_tag else "Không có giá"

            # Lấy phần trăm giảm giá
            discount_percent_tag = product.find("div", class_="price-discount__percent")
            discount_percent = discount_percent_tag.text.strip() if discount_percent_tag else "Không có giảm giá"

            # Lấy số lượng đã bán
            sold_tag = product.find("span", class_="quantity")
            sold = sold_tag.text.replace("Đã bán", "").strip() if sold_tag else "Không có thông tin bán"

            # Lấy thương hiệu
            brand_tag = product.find("div", class_="style__AboveProductNameStyled-sc-m30gte-0")
            brand = brand_tag.text.strip() if brand_tag else "Không có thương hiệu"

            # Thêm dữ liệu vào danh sách
            product_data.append((title, price, discount_percent, sold, brand, link))


page_number=int(input('Nhập số trang cần lấy dữ liệu: '))
search_keyword=input('Nhập từ khóa tìm kiếm: ')


# Crawl dữ liệu từ Lazada
crawl_lazada(page_number,product_data_lazada,search_keyword)
# Crawl dữ liệu từ Sendo
crawl_sendo(page_number,product_data_sendo,search_keyword)
# Crawl dữ liệu từ Tiki
crawl_tiki(page_number,product_data_tiki,search_keyword)

# In số lượng sản phẩm đã lấy được
print("Số lượng sản phẩm Lazada:", len(product_data_lazada))
print("Số lượng sản phẩm Sendo:", len(product_data_sendo))
print("Số lượng sản phẩm Tiki:", len(product_data_tiki))


# Hiển thị dữ liệu
import pandas as pd
df_lazada=pd.DataFrame(product_data_lazada,columns=["title","price","sold","rating","location","link"])
df_sendo=pd.DataFrame(product_data_sendo,columns=["title","original_price","discount_price","discount_percent","location","link"])
df_tiki=pd.DataFrame(product_data_tiki,columns=["title","price","discount_percent","sold","brand","link"])
print(df_lazada.head(10))
print(df_sendo.head(10))
print(df_tiki.head(10))

# Lưu dữ liệu vào file CSV
df_lazada.to_csv(f"./data_crawler/lazada/{search_keyword}_lazada_data.csv", index=False,encoding='utf-8')
df_sendo.to_csv(f"./data_crawler/sendo/{search_keyword}_sendo_data.csv", index=False,encoding='utf-8')
df_tiki.to_csv(f"./data_crawler/tiki/{search_keyword}_tiki_data.csv", index=False,encoding='utf-8')

# Đóng trình duyệt
driver.quit()