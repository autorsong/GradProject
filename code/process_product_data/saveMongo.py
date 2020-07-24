#-*- coding: utf-8 -*-

#처음의 사용자의 전체 로그에서 유효한 검색 기록, 클릭 기록만 다시 재저장하는 코드

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from pymongo import MongoClient

client = MongoClient('localhost')
db = client.test

client2 = MongoClient('localhost')
db2 = client2.test

dic = {}
for i, r in enumerate(db.local.find({})):	
	try:		
		seq = r['MBER_SEQ']
		
		if len(seq) < 1:
			continue
		
		try:
			word = r['new_query_string']['SEARCH_NM']

		except:
			try:
				word = r['new_query_string']['PROD_CODE']
				
				if len(word) != 14:
					continue

			except Exception, e:
				print "ERROR1 : " + str(e)

		finally:
			db2.main.insert(r)

	except Exception, e:
		print "ERROR2 : " + str(e)