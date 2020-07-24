#-*- coding: utf-8 -*-

#read_mongo_text.py에서 사용자의 기록에서 추출가능한 명사를 카운팅 한 것 처럼, 상품의 정보에서 추출되는 명사들 또한 카운팅해서 db에 저장하는 코드.

import sys  
import pymysql
from konlpy.tag import Twitter
from pymongo import MongoClient
import json
import twitter_korean
import re


reload(sys)  
sys.setdefaultencoding('utf8')

db_conn = pymysql.connect()
cursor = db_conn.cursor(pymysql.cursors.DictCursor)
cursor.execute("select prod_code, prod_nm, keyword from Product_info;")
rows = cursor.fetchall()

hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')

dic = {}
for i, row in enumerate(rows):
	print i

	prod_code = str(row["prod_code"])
	dic[prod_code] = []
	tList = []

	word = str(row["prod_nm"]) + str(row["keyword"])
	word = twitter_korean.normalize(word) # 오타 처리 

	temp = ""
	for w in hangul.findall(word):
		temp += " " + w
	temp += hangul.sub('', word) # 영어 처리


	templist1 = Twitter().pos(temp)
	for value in templist1:
		if value[1] == "Noun" or value[1] == "Alpha":
			if len(value[0]) > 1:
				tList.append(value[0].encode('utf-8'))

	dic[prod_code] = tList

db_conn.commit()
db_conn.close()

for key in dic.keys():
	remove_overlap = list(set(dic[key]))
 
	temp = {}
	 
	for list_name in remove_overlap:
	    temp[list_name] = 0
	 
	for list_count in dic[key]:
	    temp[list_count] = temp[list_count] + 1

	dic[key] = temp

connect = MongoClient('166.104.140.76', 61000)
db = connect['capstone_db']
db.authenticate('capstone','capstonepwd')

for k,v in dic.items():

	string = '{"PROD_CODE" : ' + str(k) + ', "LOG" : {'
	check = 1
	for i,j in v.items():
		check = 0
		string += '"' +  i + '" : ' + str(j) + ', '

	if check: # 명사가 아무것도 없을 시
		continue

	string = string[:-2] + '}'
	string += '}'

	try:
		string = json.loads(string)
		db.tempProduct.insert(string)
	except Exception,e:
		print string
		print str(e)

