import requests
import lxml.html
import csv
import os
from tenacity import retry,stop_after_attempt

from captcha.handle_captcha import Handler

proxy_pool=[
('61.135.217.7', 80),
('122.114.31.177', 808)
]

class JobDownload():
    def __init__(self, job_category, position,path ,header, s,city_name,proxy=None, city=101040100):
        self.city = city
        self.position = position
        self.job_category = job_category
        self.path=path
        self.header=header
        self.proxy=proxy
        self.s=s    #二级类型
        self.city_name=city_name

        self.START_URL = 'https://www.zhipin.com/job_detail/?query=&scity={}&industry=&position={}'.format(city,
                                                                                                           position)
        self.ROOT_URL = 'https://www.zhipin.com'
        self.page = 0
        self.job_infos = set()
        self.sort = 1

    @retry(stop=stop_after_attempt(3))
    def download_page(self, url):
        return requests.get(url, headers=self.header,proxies=self.proxy)

    def extract_each_job(self, job):
        # 职位
        job_title = job.xpath(".//div[@class='job-title']/text()")[0]
        # 薪资
        salary = job.xpath(".//span[@class='red']/text()")[0]
        low, high = salary.split("-")[0].split("k")[0], salary.split("-")[-1].split("k")[0]
        low, high = int(low) * 1000, int(high) * 1000

        # 城市 工作经验 学历要求
        t1 = job.xpath(".//div[@class='info-primary']/p/text()")
        try:
            city, exp, edu = t1[0].strip(), t1[1], t1[2]
        except:
            city, exp, edu = t1[0].strip(),  t1[1],'不限'
        # 公司名称
        company = job.xpath(".//div[@class='company-text']/h3/a/text()")[0]
        # 公司行业 融资阶段 公司规模
        t2 = job.xpath(".//div[@class='company-text']/p/text()")
        industry, scale = t2[0], t2[-1]
        status = t2[1] if len(t2) == 3 else '融资情况未知'

        url = job.xpath(".//h3[@class='name']/a/@href")[0]
        url = url.split('/')[-1].split('~.')[0]

        job_info = (self.s, self.job_category, job_title, low, high, city, exp, edu, company, industry, status, scale, url)
        return job_info

    def parse_each_page(self, html):
        self.page += 1
        tree = lxml.html.fromstring(html)

        captcha=tree.xpath("//*[@id='wrap']/div/div/text()")
        if len(captcha) != 0:
            print(captcha[0])
            if captcha[0] == "为了您的账号安全，我们需要在执行操作之前验证您的身份，请输入验证码。":
                captcha_handler = Handler()
                captcha_handler.execute()
                return 'parse again'

        jobs = tree.xpath("//div[@class='job-primary']")

        if not len(jobs):
            return None
        for job in jobs:
            job_info = self.extract_each_job(job)
            # 将数据写入csv
            self.job_infos.add(job_info)

        print("已爬取{}第{}页信息".format(self.job_category, self.page))
        try:
            if tree.xpath("//div[@class='page']/a/@class")[-1] == 'next disabled':
                if self.page == 10 and self.sort == 1:
                    self.sort = 2
                    return 'https://www.zhipin.com/c{}-p{}/h_{}/?page=1&sort=2&ka=page-1'.format(self.city, self.position,
                                                                                                 self.city)
                return None
        except:
                return None
        # 休息你mb
        # time.sleep(random.randrange(3, 6))
        return self.ROOT_URL + tree.xpath("//div[@class='page']/a/@href")[-1]

    def run(self):
        url = self.START_URL
        writer = csv.writer(open('{}\\{}{}.csv'.format(self.path, self.job_category.replace('/', '_'),self.city_name), 'w',
                                 newline='', encoding='utf-8-sig'))
        fields = ('类型', '职位类型', '职位', '最低薪资', '最高薪资', '城市', '工作经验', '学历要求', '公司名称', '公司行业', '融资阶段', '公司规模', 'URL')
        writer.writerow(fields)
        while url:
            html = self.download_page(url)
            #print(html.status_code)
            return_url=self.parse_each_page(html.text)
            if return_url == 'parse again':
                self.page-=1
                continue
            url = return_url

        for job in self.job_infos:
            writer.writerow(job)
        print(f"成功爬取{self.job_category}所有职位信息")
        #print('成功爬取{}所有职位信息'.format(self.job_category))


if __name__ == '__main__':
    job_category = "c++"
    position = "100102"

    job = JobDownload(job_category, position,path='job_tables')
    job.run()


