import re
import time
import hashlib
import requests


def use_get():
    response = requests.get('https://www.lejobadequat.com/emplois')
    print('Status Code:', response.status_code)
    print('Content HTML:', response.text)


# def use_post():
#     payload = {
#         "action": "facetwp_refresh",
#         "data": {
#             "facets": {
#                 "recherche": [],
#                 "ou": [],
#                 "type_de_contrat": [],
#                 "fonction": [],
#                 "load_more": [
#                     2
#                 ]
#             },
#             "frozen_facets": {
#                 "ou": "hard"
#             },
#             "http_params": {
#                 "get": [],
#                 "uri": "emplois",
#                 "url_vars": []
#             },
#             "template": "wp",
#             "extras": {
#                 "counts": True,
#                 "sort": "default"
#             },
#             "soft_refresh": 1,
#             "is_bfcache": 1,
#             "first_load": 0,
#             "paged": 2
#         }
#     }
#     response = requests.post('https://www.lejobadequat.com/emplois', json=payload)
#     print('Status Code:', response.status_code)
#     content = response.json()['template']
#     print('Content:', response.json()['template'])
#     print('Grutier au sol  H/F' in content)


def use_header():
    pattern = '<th>USER-AGENT<\/th>\s*<td><span class="code detected_result">(.+)<\/span><\/td>'

    response = requests.get('https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/')
    user_agent = re.search(pattern, response.text).group(1)
    print('Default useragent:', user_agent)

    time.sleep(2)

    response = requests.get(
        url='https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    )

    # print(response.text)
    user_agent = re.search(pattern, response.text).group(1)
    print('Changed useragent:', user_agent)


def use_proxy():
    # response = requests.get('https://2ip.io/')
    # print(response.text)

    proxy = '152.42.229.153'
    port = 3128

    proxies = {
        'http': f'http://{proxy}:{port}',
        'https': f'http://{proxy}:{port}'
    }

    response = requests.get(
        url='https://2ip.io/',
        proxies=proxies,
        timeout=30,
        headers={'User-Agent': 'python-requests/2.32.3'}
    )
    print(response.text)


# def get_content(url):
#     # 1. check file
#     # 2. make request and save content
#     filename = hashlib.md5(url.encode('utf-8')).hexdigest()
#     try:
#         with open(filename, 'r') as f:
#             content = f.read()
#             print('get from file')
#             return content
#     except:
#         response = requests.get(url)
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(response.text)
#         print('get from server')
#         return response.text


if __name__ == '__main__':
    # use_get()
    # use_post()
    # use_header()
    use_proxy()
    # content = get_content('https://www.lejobadequat.com/emplois')
