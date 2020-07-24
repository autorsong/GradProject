#-*- coding: utf-8 -*-
import gensim
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


### sentence class
class MySentences(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def __iter__(self):
        for line in codecs.open(self.filepath, encoding='utf-8'):
            yield line.split(' ')

sentences_vocab = MySentences('../../data/corpus/processed/corpus_pos.txt')
sentences_train = MySentences('../../data/corpus/processed/corpus_pos.txt')

### training model
model = gensim.models.Word2Vec()
model.build_vocab(sentences_vocab)
model.train(sentences_train, total_examples=model.corpus_count, epochs=10)

### save trained model
model.save('../../data/nlp/model')
