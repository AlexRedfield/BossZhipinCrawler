#!/usr/bin/env python
# coding:utf-8
'''该模块用于处理验证码'''

import requests
import pandas as pd
from hashlib import md5


class Chaojiying_Client():
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')

        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }


    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()


    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    id1=auth_token = pd.read_csv('D:/Documents/token/id1.txt', header=None)[0][0]
    id2 = auth_token = pd.read_csv('D:/Documents/token/id2.txt', header=None)[0][0]
    chaojiying = Chaojiying_Client(f'{id1}', 'chaojiying', f'{id2}')
    im = open('captcha.jpg', 'rb').read()
    result=chaojiying.PostPic(im, 1902)
    print(result['pic_str'])

