import requests
import json
from bs4 import BeautifulSoup
import re
import csv

# Get API of each product
def get_product_url(product_urls: list, keyword: str, page_number: int):

    category_url = f'https://searchlist-api.sendo.vn/web/products?q={keyword}&platform=web&page={page_number}&size=60&sortType=rank'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://www.sendo.vn/',
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    }  
    response=requests.get(category_url,headers=headers)
    if response.status_code==200:
        data_res=json.loads(response.text)
        data = data_res['data']

    category_paths = [item['category_path'] for item in data]
    product_urls.extend([f"https://detail-api.sendo.vn/full/{product_path.replace('.html', '')}" for product_path in category_paths])

# Get detail of product with API
def get_product_detail(product_url: str, output_file: str):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://www.sendo.vn/',
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    }  
    response=requests.get(product_url,headers=headers)
    if response.status_code==200:
        data_res=json.loads(response.text)
        data = data_res['data']
        # Extract required fields
        product_data = {
            "productID": data.get("id"),
            "productName": data.get("name"),
            "productURL": data.get("url_key"),
            "productImage": data.get("image"),
            "productRating": data.get("rating_info", {}).get("percent_star"),
            "productNumRate": data.get("rating_info", {}).get("total_rated"),
            "productNumSold": data.get("order_count"),
            "productBrand": data.get("brand_info", {}).get("name"),
            "categoryID": data.get("category_id"),
            "categoryInfo": json.dumps(data.get("category_info", []), ensure_ascii=False),
            "productOrgPrice": data.get("price"),
            "productCrtPrice": data.get("final_price"),
            "sellerID": data.get("shop_info", {}).get("shop_id"),
            "sellerName": data.get("shop_info", {}).get("shop_name"),
            "sellerURL": data.get("shop_info", {}).get("shop_url"),
            "sellerRating": data.get("shop_info", {}).get("rating_avg"),
            "sellerType": json.dumps([badge.get("type") for badge in data.get("shop_info", {}).get("shop_badge_urls", [])]),
            "sellerLocation": data.get("shop_info", {}).get("warehourse_region_name"),
            "inventoryStatus": data.get("stock_status"),
            "inventoryStock": data.get("quantity"),
            "promotion": data.get("promotion_percent"),
        }
        # Write data to CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=product_data.keys())
            writer.writeheader()
            writer.writerow(product_data)
        
        print(f"Data saved to {output_file}")


