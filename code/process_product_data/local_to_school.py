#-*- coding: utf-8 -*-
import sys 

#로컬에서 작업한 것 연구실 db로 옮기는 코드

reload(sys)  
sys.setdefaultencoding('utf8')

from pymongo import MongoClient

client = MongoClient('localhost')
db = client.test

connect = MongoClient()
db2 = connect['capstone_db']
db2.authenticate('capstone','capstonepwd')

for i, row in enumerate(db.checkmodule.find()):
	print i
	db2.checkmodule.insert(row)