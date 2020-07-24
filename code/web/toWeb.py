#-*- coding: utf-8 -*-
#연구실 디비에 있는 것을 php에서 읽어오는 폼대로 데이터 수정해서 로컬에 저장하는 코드
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from pymongo import MongoClient

client = MongoClient('localhost')
db = client.test

connect = MongoClient()
db2 = connect['capstone_db']
db2.authenticate('capstone','capstonepwd')

for i, row in enumerate(db2.recommendProduct2.find()):
	dic = {}
	if(len(row["recommended_item"]) == 0):
		continue
	else:
		dic["MBER_SEQ"] = str(row["mber_seq"])
		temp = []
		for item in row["recommended_item"]:
			temp.append(str(item["prod_code"])[:14])
		dic["Product"] = temp

	db.final2.insert(dic)