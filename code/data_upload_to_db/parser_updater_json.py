#-*- coding: utf-8 -*-
from pymongo import MongoClient
import json

#회원의 로그 기록에 한하여 MBER_SEQ, uri, referer, new_query_string을 뽑아 txt파일에 저장
filepath = '../../data/ssocio_info/'
user_log_filename = '20160701~20160930.json'

connect = MongoClient()
db = connect['capstone_db']
db.authenticate('capstone', 'capstonepwd')

with open(filepath + 'json_final.txt', 'w') as writefile:
    with open(filepath + user_log_filename) as readfile:
        for i, line in enumerate(readfile):
            if(i < 3):
                continue

            checkString = line[line.find('"MBER_SEQ"'):line.find(',', line.find('"MBER_SEQ"'))]
            if(checkString == '"MBER_SEQ" : "-"'):
                continue
            else:
                jsonString = "{ " + line[line.find('"uri"'):line.find(',', line.find('"uri"'))] + ", "
                jsonString += line[line.find('"referer"'):line.find(',', line.find('"referer"'))] + ", "

                if(line.find('"new_query_string"') == -1):
                    jsonString += line[line.find('"MBER_SEQ"'):line.find(',', line.find('"MBER_SEQ"'))] + " }\n"
                else:
                    jsonString += line[line.find('"MBER_SEQ"'):line.find(',', line.find('"MBER_SEQ"'))] + ", "
                    jsonString += line[line.find('"new_query_string"'):]

                writefile.write(jsonString)

#이를 db에 저장
count = 0
with open(filepath + 'json_final.txt', 'r') as readfile:
    for i, line in enumerate(readfile):
        try:
            o = json.loads(line)
            db.checkModule.insert(o)
        except:
            count = count + 1
        finally:
            print i

print count + " log records are inserted."

#데이터들 중, SEARCH_NM / PROD_CODE 가진 로그 기록만 다시 뽑아 test db에 넣음
db = client.local
db2 = client.test

count = 0
for i, line in enumerate(db.local.find({})):
    print i
    try:
        temp = line['new_query_string']['SEARCH_NM']
        db2.local.insert(line)
    except Exception, e:
        try:
            temp = line['new_query_string']['PROD_CODE']
            db2.local.insert(line)

        except Exception, e:
            count += 1

print count
