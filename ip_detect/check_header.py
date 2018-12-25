import codecs
import json
import requests
import pandas

df=pandas.read_csv('headers.csv')

headers=[i for i in df['User-Agent']]

#header=random.choice(headers)
for i,header in enumerate(headers):
    #header=headers[0]
    header={'User-Agent': header}

    url='https://www.zhipin.com/job_detail/?query=&scity=101040100&industry=&position=100101'
    response = requests.get(url,
                            headers=header,
                            timeout=10)
    html_doc = response.status_code
    print(html_doc,i,header)
