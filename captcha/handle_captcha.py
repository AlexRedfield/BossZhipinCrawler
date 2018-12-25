import time
import pandas as pd
from selenium import webdriver
from PIL import Image
from captcha.chaojiying import Chaojiying_Client


class Handler():
    def __init__(self):
        url = 'https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D'
        self.driver = webdriver.Chrome()
        self.driver.get(url=url)

    def save_captcha(self):
        # 截取验证码图片并保存到本地
        self.driver.save_screenshot('captcha.png')
        img = self.driver.find_element_by_xpath("//*[@id='wrap']/div/form/p/img")

        left = img.location['x']
        top = img.location['y']
        right = img.location['x'] + img.size['width']
        bottom = img.location['y'] + img.size['height']

        im = Image.open('captcha.png')
        im = im.crop((left, top, right, bottom))
        im.save('captcha.png')

    def get_code(self):
        id1 = pd.read_csv('D:/Documents/token/id1.txt', header=None)[0][0]
        id2 = pd.read_csv('D:/Documents/token/id2.txt', header=None)[0][0]
        chaojiying = Chaojiying_Client(f'{id1}', 'chaojiying', f'{id2}')
        im = open('captcha.png', 'rb').read()
        result = chaojiying.PostPic(im, 1902)
        return result['pic_str']

    def input(self, value):
        # 将api返回的验证码输入
        elem = self.driver.find_element_by_id('captcha')
        elem.send_keys(value)
        self.driver.find_element_by_tag_name('button').click()

    def execute(self):
        self.save_captcha()
        self.input(self.get_code())
        time.sleep(1)
        self.driver.close()


if __name__ == '__main__':
    captcha_handler = Handler()
    captcha_handler.execute()
