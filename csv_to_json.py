import pandas as pd
import io
import json
import codecs


def eli_dup(origin_list):
    result_list = list(set(origin_list))
    result_list.sort(key=origin_list.index)
    return result_list


# 写入带中文字符的json 文件
def jump_json(filename, sre):
    jsonFile = io.open(filename, 'w', encoding='utf8')
    jsonFile.write(json.dumps(sre, ensure_ascii=False))
    jsonFile.flush()
    jsonFile.close()


df = pd.read_csv('data.csv', encoding='gb18030')


def get_class():
    class1 = df['class_1']
    class2 = df['class_2']

    b1, s1 = [], []
    for i in class1:
        b1.append(i)

    for i in class2:
        s1.append(i)

    b2, s2 = eli_dup(b1), eli_dup(s1)
    b2.sort(key=b1.index)  # class_1 的数组
    s2.sort(key=s1.index)  # class_2 的数组
    return b2, s2


ds = {}


# 创造第一层数据结构
def create_level1(b2):
    for j in b2:
        result = df['class_2'][df.class_1 == j]
        result = [i for i in result]
        result = eli_dup(result)  # 它改变了数组
        result = [{i: None} for i in result]  # 它又变了回来
        ds[j] = result


# 创造第二层数据结构
def create_level2(ds):
    for b in ds:  # b是单个大类
        for s in ds[b]:  # s是单个小类 {"后端开发": null}
            s0 = list(s.keys())[0]  # 后端开发
            r1, r2 = df['name'][df.class_2 == s0], df['id'][df.class_2 == s0]
            result1, result2, result0 = [i for i in r1], [i for i in r2], [0 for i in r1]
            result = list(zip(result1, result2, result0))  # [('Java', 100101), ('C++', 100102),...]
            s[s0] = result


# 写入json
def dump_json():
    with codecs.open('ds.json', 'w', 'utf-8') as f:
        json.dump(ds, f, ensure_ascii=False)


if __name__ == '__main__':
    b2, s2 = get_class()
    create_level1(b2)
    create_level2(ds)

    dump_json()
