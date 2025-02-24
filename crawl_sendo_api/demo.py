import requests
import json
def crawl_api():
    url='https://detail-api.sendo.vn/full/den-ban-led-rang-dong-cam-ung-model-rl45-6w-115971194?source_block_id=feed&source_page_id=search&source_info=desktop2_60_1740368290557_4eae965a-ca1d-4333-a520-1a141c3eeca6_-1_cateLvl2_0_1_23_-1&platform=web'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://tiki.vn/thoi-trang-nam/c915',
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
}
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        data=json.loads(response.text)
        print(data['data'])

crawl_api()