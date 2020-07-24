#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from konlpy.tag import Twitter
import codecs

tagger = Twitter()


def flat(content):
    return ["{}/{}".format(word, tag) for word, tag in tagger.pos(content)]

corpus = codecs.open('../../data/corpus/processed/corpus_pos.txt', 'w', encoding='utf-8')
with open('../../data/corpus/processed/corpus.txt', 'r') as readfile:
    for line in readfile:
        corpus.write((' '.join(flat(line))).encode('utf-8') + '\n')
