import requests
import json
from bs4 import BeautifulSoup
import re

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
def get_product_detail(product_url: str, product_data: list):
    
    product_url = 'https://detail-api.sendo.vn/full/nghe-thuat-an-trua-ban-cong-viec-moi-90-hcm0103-116096826'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://www.sendo.vn/',
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    }  
    response=requests.get(product_url,headers=headers)
    if response.status_code==200:
        data_res=json.loads(response.text)
        # print(data_res['data'])
        print(data_res['data'].keys())

product_data=[]
product_url = ''
get_product_detail(product_url, product_data)