import codecs
import json

'''清空记录json中的值'''

with codecs.open('ds.json', 'r','utf-8') as f:
    data = json.load(f)

for s in data['技术']:
    for s_name in s:
        job_list=s[s_name]
        for job_info in job_list:

            job_info[-1] = 0
with codecs.open('ds.json', 'w', 'utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
