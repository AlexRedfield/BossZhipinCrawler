import time
from selenium import webdriver
from PIL import Image
from captcha.chaojiying import Chaojiying_Client


class Handler():
    def __init__(self):
        url = 'https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D'
        self.driver = webdriver.Chrome()
        self.driver.get(url=url)

    def save_captcha(self):
        self.driver.save_screenshot('captcha.png')
        img = self.driver.find_element_by_xpath("//*[@id='wrap']/div/form/p/img")

        left = img.location['x']
        top = img.location['y']
        right = img.location['x'] + img.size['width']
        bottom = img.location['y'] + img.size['height']

        im = Image.open('captcha.png')
        im = im.crop((left, top, right, bottom))
        im.save('captcha.png')

    def input(self, value):
        elem = self.driver.find_element_by_id('captcha')
        elem.send_keys(value)
        self.driver.find_element_by_tag_name('button').click()

    def get_code(self):
        chaojiying = Chaojiying_Client('alex877428', 'chaojiying', '96001')
        im = open('captcha.png', 'rb').read()
        result = chaojiying.PostPic(im, 1902)
        return result['pic_str']

    def execute(self):
        self.save_captcha()
        self.input(self.get_code())
        time.sleep(1)
        self.driver.close()


if __name__ == '__main__':
    captcha_handler = Handler()
    captcha_handler.execute()
