#-*- coding: utf-8 -*-

from pymongo import MongoClient
import json

client = MongoClient('localhost')
db = client.test

count = 0
with open('json_final.txt', 'r') as readfile:
	for i, line in enumerate(readfile):
		try:
			o = json.loads(line)
			db.local.insert(o)
		except:
			count = count + 1
		finally:
			print i

print count