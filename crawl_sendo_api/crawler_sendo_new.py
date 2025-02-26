import requests
import json
import csv
import time

# Get product URLs from keyword and number of pages
def get_product_urls(keyword: str, num_pages: int):
    product_urls = []
    
    for page_number in range(1, num_pages + 1):
        category_url = f'https://searchlist-api.sendo.vn/web/products?q={keyword}&platform=web&page={page_number}&size=60&sortType=rank'
        print(f"Getting data from {category_url}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Referer': 'https://www.sendo.vn/',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
        }

        response = requests.get(category_url, headers=headers)

        if response.status_code == 200:
            data_res = json.loads(response.text)
            data = data_res.get('data', [])

            for item in data:
                product_path = item.get('category_path', '').replace('.html', '')
                if product_path:
                    product_urls.append(f"https://detail-api.sendo.vn/full/{product_path}")
        else:
            print(f"Eror: {response.status_code}")
        
        time.sleep(2) 
    return product_urls

# Get product details from API
def get_product_details(product_url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Referer': 'https://www.sendo.vn/',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
    }
    
    response = requests.get(product_url, headers=headers)

    if response.status_code == 200:
        data_res = json.loads(response.text)
        data = data_res.get('data', {})
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
            # "sellerType": json.dumps([badge.get("type") for badge in data.get("shop_info", {}).get("shop_badge_urls", [])]),
            "sellerType": json.dumps([badge.get("type") for badge in (data.get("shop_info", {}).get("shop_badge_urls") or [])]),
            "sellerLocation": data.get("shop_info", {}).get("warehourse_region_name"),
            "inventoryStatus": data.get("stock_status"),
            "inventoryStock": data.get("quantity"),
            "promotion": data.get("promotion_percent"),
        }
        return product_data
    
    else:
        print(f"Error: {response.status_code}")

    return None

# Crawl all products and save to CSV file
def crawl_sendo_products(keywords: list[str], num_pages: int, output_file: str):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = None
    
        for keyword in keywords:
            product_urls = get_product_urls(keyword, num_pages)
            
            if not product_urls:
                print("No product found")
                continue
            
            for index, product_url in enumerate(product_urls, start=1):
                product_data = get_product_details(product_url)
                
                if product_data:
                    if writer is None:
                        writer = csv.DictWriter(file, fieldnames=product_data.keys())
                        writer.writeheader()
                    
                    writer.writerow(product_data)
                    print(f"({index}/{len(product_urls)}) Saved: {product_data['productName']}")

                time.sleep(2)  

    print(f"Saved data into {output_file}")

keyword = ["nội thất", "bàn phím"]
num_pages = 1
output_file = "sendo_products.csv"

crawl_sendo_products(keyword, num_pages, output_file)
