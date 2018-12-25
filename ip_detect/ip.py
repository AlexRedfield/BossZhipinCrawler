import requests
import pandas
import random

url = 'https://www.zhipin.com/c101010100-p100101/'
#url='https://www.163.com'


def detect_ip(i):
    ip, port = i

    proxy_url = "http://{0}:{1}".format(ip, port)

    proxy_dict = {
        "http": proxy_url
    }
    try:
        response = requests.get(url, headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        },proxies=proxy_dict,timeout=5)
        html_doc = response.status_code
        print(i, html_doc)
    except:
        print(i,'fails')


#for i in results:

i=('120.25.203.182', 7777)
i=('120.25.203.182', 7777)
detect_ip(i)


