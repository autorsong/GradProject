#-*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from pymongo import MongoClient
import pymysql

client = MongoClient('localhost')
db = client.test

db_conn = pymysql.connect()
cursor = db_conn.cursor(pymysql.cursors.DictCursor)

dic = []
for i, r in enumerate(db.local.find({})):	
	try:
		print i

		if i > 10000:
			break
		
		try:
			word = r['new_query_string']['SEARCH_NM']

			dic.append(word.encode('utf-8'))

		except:
			try:
				word = r['new_query_string']['PROD_CODE']

				sql = "select prod_nm, keyword from Product_info where prod_code=" + word + ";"
				cursor.execute(sql)
				result = cursor.fetchone()

				word1 = result['prod_nm']
				word2 = result['keyword']

				if word1 != None:
					dic.append(word1.encode('utf-8'))

				if word2 != None:
					dic.append(word2.encode('utf-8'))			

			except Exception, e:
				print "ERROR1 : " + str(e)
			

	except Exception, e:
		print "ERROR2 : " + str(e)

db_conn.commit()
db_conn.close()

dic = list(set(dic))

f = open('temp_testing.txt','w')
for v in dic:
	string = v + "\n"
	f.write(string)

f.close()