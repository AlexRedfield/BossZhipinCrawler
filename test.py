import pandas as pd
import io
import json
import codecs
import lxml.html
import requests
import os
import pymysql

'''
url='https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D'
html=requests.get(url).text
tree = lxml.html.fromstring(html)

try:
    capcha = tree.xpath("//*[@id='wrap']/div/div/text()")[0]
    print(capcha)
    if capcha== "为了您的账号安全，我们需要在执行操作之前验证您的身份，请输入验证码。":
        print(1)
        os._exit(0)
    else:
        print(2)
except:

    print("为了您的账号安全，我们需要在执行操作之前验证您的身份，请输入验证码。")

'''

a='abc'
time=20
c=f"have {time} {a}"
print(c)
