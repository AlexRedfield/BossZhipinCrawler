# -*- coding:utf8 -*-

import requests
import socket
socket.setdefaulttimeout(3)

inf = open("ip.txt")    # 这里打开刚才存ip的文件
lines = inf.readlines()
proxys = []
for i in range(0,len(lines)):
    proxy_host = "http://" + lines[i].strip()
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)

# 用这个网页去验证，遇到不可用ip会抛异常
url = "http://ip.chinaz.com/getip.aspx"
#url="https://www.zhipin.com/c101010100-p100101/"
# 将可用ip写入valid_ip.txt
ouf = open("valid_ip.txt", "a+")

for proxy in proxys:
    try:
        res = requests.get(url,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        },proxies=proxy, timeout=5)
        valid_ip = proxy['http'][7:]
        print('valid_ip: ' + valid_ip + ' ' + str(res.status_code))
        if res.status_code == 200:
            ouf.write(valid_ip)
    except Exception as e:
        print(proxy, e)
        continue
