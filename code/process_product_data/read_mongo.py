#-*- coding: utf-8 -*-

#saveMongo.py를 통해 저장한 데이터를 읽어와 txt파일로 저장하는 코드(mongo db에서 바로 읽을 경우 뒤에 처리가 잘 안됐어서 이런 번거로움을 했었음.)

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from pymongo import MongoClient
import pymysql
from konlpy.tag import Twitter
import pprint

client = MongoClient('localhost')
db = client.test


dic = {}
for i, r in enumerate(db.main.find({})):	
	try:		
		seq = r['MBER_SEQ']
		if dic.get(seq, -1) == -1:
			dic[seq] = []
		
		try:
			word = r['new_query_string']['SEARCH_NM']
			dic[seq].append(word.encode('utf-8'))

		except:
			try:
				word = r['new_query_string']['PROD_CODE']
				dic[seq].append(word.encode('utf-8'))

			except Exception, e:
				print "ERROR1 : " + str(e)


	except Exception, e:
		print "ERROR2 : " + str(e)



f = open('read_mongo.txt','w')
for k,v in dic.items():
	string = k + " : ["
	for t in v:
		string += t + ","
	string = string[:-1]
	string += "]\n"

	f.write(string)

f.close()