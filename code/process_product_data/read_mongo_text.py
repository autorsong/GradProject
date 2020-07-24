#-*- coding: utf-8 -*-

#read_mongo.py에서 만든 txt파일을 읽어, 사용자마다의 검색&클릭 기록에서 추출되는 명사들을 뽑아 카운팅 후, db에 저장

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

hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')

dic = {}
with open('read_mongo.txt','r') as readfile:
	for i, line in enumerate(readfile):
		print i

		mber_seq = line[0:line.find(' : ')]
		dic[mber_seq] = []

		temp = line[line.find(' : [')+4:line.find(']')]
		valueList = temp.split(',')

		for word in valueList:
			tList = []

			if word[:3] == "201" and len(word) == 14: #PROD_CODE 일 때
				sql = "select prod_nm, keyword from Product_info where prod_code=" + word + ";"
				cursor.execute(sql)
				result = cursor.fetchone()

				if result == None: # 상품이 엑셀에 없을 때
					continue

				word1 = result['prod_nm']
				word2 = result['keyword']

				if word1 != None:
					try:
						word = twitter_korean.normalize(word1) # 오타 처리 

						temp = ""
						for w in hangul.findall(word):
							temp += " " + w
						temp += hangul.sub('', word) # 영어 처리


						templist1 = Twitter().pos(temp)
						for value in templist1:
							if value[1] == "Noun" or value[1] == "Alpha":
								if len(value[0]) > 1:
									tList.append(value[0].encode('utf-8'))
					except Exception, e:
						print "ERROR[1] : " + str(e)

				if word2 != None:
					try:
						word = twitter_korean.normalize(word2) # 오타 처리 

						temp = ""
						for w in hangul.findall(word):
							temp += " " + w
						temp += hangul.sub('', word) # 영어 처리


						templist1 = Twitter().pos(temp)
						for value in templist1:
							if value[1] == "Noun" or value[1] == "Alpha":
								if len(value[0]) > 1:
									tList.append(value[0].encode('utf-8'))
					except Exception, e:
						print "ERROR[2] : " + str(e)
			else: #검색어
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

			dic[mber_seq] = tList

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

connect = MongoClient()
db = connect['capstone_db']
db.authenticate('capstone','capstonepwd')

for k,v in dic.items():

	string = '{"MBER_SEQ" : ' + k + ', "LOG" : {'
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
		db.checkmodule.insert(string)
	except Exception,e:
		print string
		print str(e)

