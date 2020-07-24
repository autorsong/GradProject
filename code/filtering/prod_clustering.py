#-*- coding: utf-8 -*-
from pymongo import MongoClient
import numpy as np
from scipy import spatial
import gensim
import sys
import json
import time
reload(sys)
sys.setdefaultencoding('utf8')

model = gensim.models.Word2Vec.load('../nlp/model')

connect = MongoClient()
db2 = connect['capstone_db']
db2.authenticate('capstone', 'capstonepwd')

no_clustering_words_list = [u"셰어/Noun", u"용품/Noun", u"판매/Noun", u"대여/Noun", u"공유/Noun", u"무료/Noun", u"상품/Noun", u"용품/Noun", u"쉐어/Noun", u"개월/Noun", u"화이트/Noun", u"그레이/Noun", u"레드/Noun", u"오렌지/Noun", u"블랙/Noun", u"옐로우/Noun", u"핑크/Noun", u"민트/Noun", u"퍼플/Noun", u"보라색/Noun"]

sim_threshold = 0.3

prod_list = []
vector_list = []
for i, prod in enumerate(db2.prodClusteredWord.find()):
    print ">>>>>>>>" + str(i)
    clustered_flag = False

    lst = []
    for wordlist in prod['wordlist']:
        for word in wordlist:
            if word['name'] not in no_clustering_words_list:
                for i in xrange(word['count']):
                    lst.append(model[word['name']])
    if len(lst) > 0:
        prod_vector = np.mean(lst, axis=0)
    else:
        prod_vector = None

    if len(vector_list) is 0:
        vector_list.append([])
        vector_list[0].append(prod_vector)
        prod_list.append([])
        prod_list[0].append(prod)
        continue

    if prod_vector is None:
        continue
    else:
        highest_similarity = float(0.0)
        highest_index = -1

        for vector_index, vector_group in enumerate(vector_list):
            similarity = 1 - spatial.distance.cosine(np.mean(vector_group, axis=0), prod_vector)

            if similarity > sim_threshold:
                clustered_flag = True
                if similarity > highest_similarity:
                    highest_similarity = similarity

        prod_list[highest_index].append(prod)
        vector_list[highest_index].append(prod_vector)

        if clustered_flag is False:
            vector_list.append([])
            vector_list[len(vector_list)-1].append(prod_vector)
            prod_list.append([])
            prod_list[len(prod_list)-1].append(prod)

    if i > 1000:
        break

print len(prod_list)
print len(vector_list)
print ""

for group in prod_list:
    print len(group)

for i, group in enumerate(prod_list):
    collection = db2["prod_" + str(i)]
    for prod in group:
        collection.insert(prod)

with open("vector.txt", 'w') as writefile:
    for i, group in enumerate(vector_list):
        writefile.write(str(np.mean(group, axis=0).tolist()) + "\n")
