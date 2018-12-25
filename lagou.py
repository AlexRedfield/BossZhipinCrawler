import requests
import json
from bs4 import BeautifulSoup

import time
import random
from multiprocessing import Pool


def get_page(pn=1):
    print('shit')
    time.sleep(random.randint(5, 10) / 10.0)
    url1 = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'
    data = {
        'first': 'true',
        'kd': 'python',
        'pn': pn,
    }
    try:
        print('hey')
        wb_data = requests.post(url1, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        }, data=data, )
        data = json.loads(wb_data.text)
        position = data['content']['positionResult']['result']
        position_total = data['content']['positionResult']['totalCount']
        print('fuck')
        for i in position:
            print(i)
            data = {
                'companySize': i['companySize'],
                'workYear': i['workYear'],
                'education': i['education'],
                'financeStage': i['financeStage'],
                'city': i['city'],
                'district': i['district'],
                'industryField': i['industryField'],
                'positionId': i['positionId'],
                'positionName': i['positionName'],
                'jobNature': i['jobNature'],
                'companyFullName': i['companyFullName'],
                'companyLabelList': i['companyLabelList'],
                'salary': i['salary'],
                'companyShortName': i['companyShortName'],
                'positionAdvantage': i['positionAdvantage'],
            }
            get_position(data)
    except:
        time.sleep(180)
        print(data)
        pass


def get_position(data):
    url2 = 'https://www.lagou.com/jobs/{}.html'.format(data['positionId'])
    wb_data = requests.get(url2,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        })
    soup = BeautifulSoup(wb_data.text, 'lxml')
    job_bt = soup.select('#job_detail > dd.job_bt > div')[0]
    work_add = soup.select('div.work_addr')[0]
    data['job_bt'] = job_bt.get_text()
    data['work_add'] = work_add.get_text().replace(' ', '').replace('\n', '')



if __name__ == '__main__':
    start = time.time()

    get_page(1)
    # pool = Pool()
    #pool.map(get_page, range(0, 81))

    end = time.time()
    print(end - start)
