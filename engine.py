import codecs
import json
import pandas
import os
import random
from boss_recruits import JobDownload
from csv_to_json import get_class

with codecs.open('ds.json', 'r', 'utf-8') as f:
    data = json.load(f)

'''
df=pandas.read_csv('ip6.csv')

ips,ports=df['ip'], df['port']
ips,ports=[i for i in ips],[i for i in ports]
results=list(zip(ips,ports))
ip, port=random.choice(results)

proxy_url = "http://{0}:{1}".format(ip, port)

proxy_dict = {
    "http": proxy_url
}
'''


def get_random_header():
    df = pandas.read_csv('ip_detect\\headers.csv')
    headers = [i for i in df['User-Agent']]

    header = random.choice(headers)
    return {'User-Agent': header}


def city_crawl(job_info, s_name, path, city_list):
    for city in city_list:

        print(f'正在爬取{city[0]}市招聘信息')
        job = JobDownload(job_info[0], job_info[1], path, header=get_random_header(), s=s_name, city=city[1], city_name=city[0])
        job.run()



def start_crawl(b, path, city_list):
    for s in data[b]:
        for s_name in s:
            job_list = s[s_name]
            for job_info in job_list:
                if not job_info[-1]:  # 单个职位状态码为0
                    city_crawl(job_info, s_name, path=path, city_list=city_list)
                    job_info[-1] = 1
                    with codecs.open('ds.json', 'w', 'utf-8') as f:
                        json.dump(data, f, ensure_ascii=False)

city_list = [('北京',101010100),('上海',101020100),('广州',101280100),('深圳',101280600),('杭州',101210100),
             ('西安',101110100),('成都',101270100)]

'''
class1, class2 = get_class()
path = 'job_tables'
if not os.path.exists(path):
    os.mkdir(path)
'''

