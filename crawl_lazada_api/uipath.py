import requests
import time
import json

# ================== THÔNG TIN CẦN THAY ĐỔI ================== 
# Nhập keyword cần tìm kiếm
keyword=input('Keyword: ')
# Loại bỏ khoảng cách trong keyword


pageNumber=int(input('Number of pages: '))

list_products = []

for i in range(1,pageNumber+1):
    keyword=keyword.replace(" ", "")
    input_arg={"keyword":keyword,"pageNumber":i}
    API_URL = "https://platform.uipath.com/uitrpa/DefaultTenant/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
    HEADERS = {
        "Content-Type": "application/json",
        "X-UIPATH-TenantName": "DefaultTenant",
        "X-UIPATH-OrganizationUnitId": "6338289",
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTkVOMEl5T1RWQk1UZEVRVEEzUlRZNE16UkJPVU00UVRRM016TXlSalUzUmpnMk4wSTBPQSJ9.eyJodHRwczovL3VpcGF0aC9lbWFpbCI6ImFuaGhpZW5kb2FuMTUwNUBnbWFpbC5jb20iLCJodHRwczovL3VpcGF0aC9lbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnVpcGF0aC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDgyMTc5NjgxOTExMjQ0MTQxNjkiLCJhdWQiOlsiaHR0cHM6Ly9vcmNoZXN0cmF0b3IuY2xvdWQudWlwYXRoLmNvbSIsImh0dHBzOi8vdWlwYXRoLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3NDA0NjUwODIsImV4cCI6MTc0MDU1MTQ4Miwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyIsImF6cCI6IjhERXYxQU1OWGN6VzN5NFUxNUxMM2pZZjYyaks5M241In0.olIpDk-0GAn99B272esKqpDMIuogbvvtNkJ3LKSvWdznb7rwhykO-nyq-y-yffZsSOXDn6B7zdUPwpOf4tCea-iIzlzocRZr_iky67_xxy6rFkNWDtKg-OXI5ECfyNI83Ah8qJwguGXNmBpkIlD8N1D1TTpKTiN2vKHubtbvhqsNn4gttZb6KCNZ6pcqtcKFQJ74EnpvOjRwbOHLqm6FHE4GY_39M-KdTaNvY3OTPJBcdZJ_Iu4GlgiveT5cyuBJop6QjYbd11aw6Kgl_LHBr8DOC6jdh11YIDr7cJyH3r-CO22JT0YuFwoRHfWWcM7Gg5dQ4Cy9jZRA-ifHT9n_xA"
    }

    PAYLOAD = {
        "startInfo": {
            "ReleaseKey": "379eb262-2acf-458c-b450-4c69414cd34e",
            "Strategy": "ModernJobsCount",
            "JobsCount": 1,
            "InputArguments": json.dumps(input_arg)  # Convert to JSON string
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=PAYLOAD)
    job_data = response.json()
    job_id = job_data["value"][0]["Id"]

    print(job_id)
    JOB_STATUS_URL = f"https://platform.uipath.com/uitrpa/DefaultTenant/odata/Jobs({job_id})"

    while True:
        job_response = requests.get(JOB_STATUS_URL, headers=HEADERS)
        job_info = job_response.json()
        state = job_info["State"]
        
        if state == "Successful":
            print("✅ Job completed successfully!")
            break
        elif state in ["Failed", "Stopped"]:
            print("❌ Job failed or was stopped.")
            exit()
        
        print("⏳ Waiting for job to complete...")
        time.sleep(3)

    output_arguments = job_info.get("OutputArguments", "{}") 

    # Chuyển đổi Output JSON (nếu cần)
    output_data = json.loads(output_arguments)

    parsed_data = json.loads(output_data["output"])  

    list_items = parsed_data["mods"]["listItems"]     

    for item in list_items:
            product_info = {
                "itemID": item.get("itemId", ""),
                "name": item.get("name", ""),
                "image": item.get("image", ""),
                "rating_score": item.get("ratingScore", ""),
                "review_count": item.get("review", ""),
                "location": item.get("location", ""),
                "seller_name": item.get("sellerName", ""),
                "brand_name": item.get("brandName", ""),
                "price": item.get("price", ""),
                "original_price": item.get("originalPrice", ""),
                "item_sold_count": item.get("itemSoldCntShow", ""),
                "categories": item.get("categories", ""),
                "promotion": item["icons"][0].get("text", "") if item.get("icons") and isinstance(item["icons"], list) and item["icons"] else "",
                "in_stock": item.get("inStock", ""),
                "stock_num":0,
                "originalPrice": item.get("originalPrice", ""),
                "itemURL": "https://www.lazada.vn" + item.get("itemUrl", "")
            }
            list_products.append(product_info)
    print("DONE CRAWLING PAGE",i)


import pandas
df=pandas.DataFrame(list_products,columns=["itemID","name","image","rating_score","review_count","location","seller_name","brand_name","price","original_price","item_sold_count","categories","promotion","in_stock","stock_num","originalPrice","itemURL"])
print(df.head())
# Save csv
df.to_csv(f'{keyword}_lazada_data.csv', index=False)




