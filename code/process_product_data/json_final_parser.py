#-*- coding: utf-8 -*-
#json_parser.py로 넣은 데이터들 중, SEARCH_NM / PROD_CODE 가진 로그 기록만 다시 뽑아 test db에 넣음

from pymongo import MongoClient
import json

client = MongoClient('localhost')
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