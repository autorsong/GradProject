#-*- coding: utf-8 -*-
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
		print i
		
		seq = r['MBER_SEQ']
		if dic.get(seq, -1) == -1:
			dic[seq] = []
		
		try:
			word = r['new_query_string']['SEARCH_NM']

			dic[seq].append(word.encode('utf-8'))

		except:
			try:
				word = r['new_query_string']['PROD_CODE']

				db_conn = pymysql.connect()
				cursor = db_conn.cursor(pymysql.cursors.DictCursor)

				sql = "select prod_nm, keyword from Product_info where prod_code=" + word + ";"
				cursor.execute(sql)
				result = cursor.fetchone()

				db_conn.commit()
				db_conn.close()

				word1 = result['prod_nm']
				word2 = result['keyword']

				try:
					if word1 != None:
						templist1 = Twitter().pos(word1)

						for value in templist1:
							if value[1] == "Noun":
								dic[seq].append(value[0].encode('utf-8'))
				except Exception, e:
					print "ERROR[1] : " + str(e)

				try:
					if word2 != None:
						templist2 = Twitter().pos(word2)

						for value in templist2:
							if value[1] == "Noun":
								dic[seq].append(value[0].encode('utf-8'))	
				except Exception, e:
					print "ERROR[2] : " + str(e)

			except Exception, e:
				print "ERROR1 : " + str(e)


	except Exception, e:
		print "ERROR2 : " + str(e)


for key in dic.keys():
	remove_overlap = list(set(dic[key]))
 
	temp = {}
	 
	for list_name in remove_overlap:
	    temp[list_name] = 0
	 
	for list_count in dic[key]:
	    temp[list_count] = temp[list_count] + 1

	dic[key] = temp

f = open('check_module_all.txt','w')
for k,v in dic.items():
	string = k + " : {"
	for i,j in v.items():
		string += "'" +  i + "' : " + str(j) + ", "
	string = string[:-2]
	string += "}\n"

	f.write(string)

f.close()