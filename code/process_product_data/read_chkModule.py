#-*- coding: utf-8 -*-
from pymongo import MongoClient
import numpy as np
from scipy import spatial
import gensim
import sys
reload(sys)
sys.setdefaultencoding('utf8')

### Word2Vec model
model = gensim.models.Word2Vec.load('../../data/nlp/model')

### MongoDB connection info
connect = MongoClient()
db2 = connect['capstone_db']
db2.authenticate('capstone', 'capstonepwd')

### similarity threshold
sim_threshold = 0.3

### ban words
no_clustering_words_list = [u"셰어/Noun", u"용품/Noun", u"판매/Noun"]


class Data:
    def __init__(self, mber_seq):
        self.mber_seq = mber_seq
        self.wordlist = []

    def __getitem__(self, key):
        if key is "mber_seq":
            return self.mber_seq
        elif key is "wordlist":
            return self.wordlist
        else:
            return None


class Word:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __getitem__(self, key):
        if key is "name":
            return self.name
        elif key is "count":
            return self.count
        else:
            return None


dic = {}
dataList = []
for i, r in enumerate(db2.tempProduct.find()):
    try:
        print i

        temp = Data(r['PROD_CODE'])
        tempWordList = []

        for k, v in r['LOG'].items():
            tempWordList.append(Word(k.encode('utf-8'), v))

        clusteredTempWordList = []
        for word in tempWordList:
            word.name = unicode(word.name, 'utf-8') + '/Noun'
            is_clstered = False

            if word.name in no_clustering_words_list:
                continue

            ### word clustering
            if word.name in model.wv.vocab:
                if len(clusteredTempWordList) is 0:
                    clusteredTempWordList.append([word])
                    continue

                for wordlist in clusteredTempWordList:
                    if not is_clstered:
                        vectorlist = []
                        for tempword in wordlist:
                            vectorlist.append(model[tempword.name])

                        ### if similarity is higher than threshold
                        if 1 - spatial.distance.cosine(np.mean(vectorlist, axis=0), model[word.name]) >= sim_threshold:
                            wordlist.append(word)
                            is_clstered = True

            else:
                continue

            if not is_clstered:
                clusteredTempWordList.append([word])

        clusteredTempWordList = [lst for lst in clusteredTempWordList if (len(lst) > 1) or (len(lst) is 1 and len(clusteredTempWordList) is 1)]
        temp.wordlist = clusteredTempWordList

        temp_dict = {}
        temp_dict["prod_code"] = temp.mber_seq
        temp_dict["wordlist"] = []
        for wordlist_iter in temp.wordlist:
            temp_wordlist = []
            for word in wordlist_iter:
                temp_word = {}
                temp_word["name"] = word.name
                temp_word["count"] = word.count
                temp_wordlist.append(temp_word)
            temp_dict["wordlist"].append(temp_wordlist)

        dataList.append(temp_dict)

    except Exception, e:
        print "ERROR : " + str(e)

### insert clustered word information to the database
for data in dataList:
    db2.prodClusteredWord.insert(data)
