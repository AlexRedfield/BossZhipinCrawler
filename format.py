import pandas as pd
import json
import io
import os
import codecs
from csv_to_json import get_class

class1,class2=get_class()
path='job_tables'
if not os.path.exists(path):
    os.mkdir(path)

with codecs.open('ds.json', 'r', 'utf-8') as f:
    data = json.load(f)

def merge(b, path):
    for s in data[b]:
        for s_name in s:
            job_list = s[s_name]        # s_name 后端开发
            for i,job_info in enumerate(job_list):
                new_path=path+'\\'+job_info[0].replace('/', '_')+'.csv'
                f=open(new_path,'r',encoding='UTF-8')
                df=pd.read_csv(f,encoding='utf-8')
                df['类型']=s_name
                df.to_csv(new_path, encoding='utf-8-sig')


for b in class1:
    path='job_tables'+'\\'+b.replace('/', '_')

    merge(b, path=path)
    print('已修改所有{}职位信息'.format(b))









