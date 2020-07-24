#-*- coding: utf-8 -*-
from pymongo import MongoClient
import numpy as np
from scipy import spatial
import gensim
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')

### import Word2Vec model
model = gensim.models.Word2Vec.load('../../data/nlp/model')

### MongoDB connection info
connect = MongoClient()
db = connect['capstone_db']
db.authenticate('capstone', 'capstonepwd')

### threshold of similarity between users and products
sim_threshold = 0.7

### processing mode
### 1 : include product words
### 2 : do not include product words
include_prod_words_mode = False


### check if user and product have same words
def user_word_check(user_wordlist, prod_wordlist):
    for uwordlist in user_wordlist:
        for pwordlist in prod_wordlist:
            for uword in uwordlist:
                for pword in pwordlist:
                    if uword['name'] == pword['name']:
                        return False
    return True


### get similarity between user and product
def user_prod_similarity(user):
    user_vector_list = []
    data_list = []

    for wordlist in user['wordlist']:
        lst = []
        for word in wordlist:
            for i in xrange(word['count']):
                lst.append(model[word['name']])
        user_vector_list.append(np.mean(lst, axis=0))

    if len(user_vector_list) is 0:
        temp_dict = {}
        temp_dict['mber_seq'] = user['mber_seq']
        temp_dict['recommended_item'] = []
        return []
    else:
        for i, prod in enumerate(db.prodClusteredWord.find()):
            prod_vector_list = []

            if (include_prod_words_mode is True) or (include_prod_words_mode is False and user_word_check(user['wordlist'], prod['wordlist'])):
                for wordlist in prod['wordlist']:
                    lst = []
                    for word in wordlist:
                        for i in xrange(word['count']):
                            lst.append(model[word['name']])
                    prod_vector_list.append(np.mean(lst, axis=0))

                for user_vector in user_vector_list:
                    for prod_vector in prod_vector_list:
                        similarity = 1 - spatial.distance.cosine(user_vector, prod_vector)
                        if similarity >= sim_threshold:
                            temp_dict = {}
                            temp_dict['prod_code'] = prod['prod_code']
                            temp_dict['similarity'] = similarity
                            data_list.append(temp_dict)

            else:
                continue

        new_data_list = sorted(data_list, key=lambda k: k['similarity'], reverse=True)
        if len(new_data_list) > 10:
            new_data_list = new_data_list[0:9]

        return new_data_list


# asdf = 11
### get recommended items for each users
for asdf in range(18, 20):
    data_list = []
    for i, user in enumerate(db.userClusteredWord.find().limit((asdf+1) * 50)):
        print ">>>>>>>>>> " + str(i)
        ### sampling users
        if i is (asdf + 1) * 50:
            connect.close()
            break
        if i < asdf * 50:
            continue
        temp_dict = {}
        temp_dict['mber_seq'] = user['mber_seq']
        temp_dict['recommended_item'] = user_prod_similarity(user)
        data_list.append(temp_dict)


    ### save recommended items to a file
    with open('recommended_product_result_' + str(asdf) + '.txt', 'w') as writefile:
        for data in data_list:
            json.dump(data, writefile)
            writefile.write('\n')

### save recommended items to the database
# with open('recommended_product_result.txt', 'r') as readfile:
#     lines = readfile.readlines()
#     for line in lines:
#         db.recommendProduct.insert(json.loads(line))
