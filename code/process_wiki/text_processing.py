#-*- coding: utf-8 -*-
import re

for i in range(0, 5):
    with open('../../data/corpus/titles_' + str(i) + '.txt', 'r') as readfile:
        with open('../../data/corpus/titles_' + str(i) + '_processed.txt', 'w') as writefile:
            pass_flag = False

            for line in readfile:
                if line.startswith("[[분류"):
                    pass_flag = False

                if line.startswith("|"):
                    continue

                if "같이 보기" in line:
                    pass_flag = True
                    continue
                if "참고 문헌" in line:
                    pass_flag = True
                    continue
                if "바깥 고리" in line:
                    pass_flag = True
                    continue

                if pass_flag is False:
                    new_line = re.sub(ur'[^가-힣 .]+', '', line.decode('utf-8'), 0, re.UNICODE).encode('utf-8')
                    writefile.write(new_line + '\n')

    with open('../../data/corpus/titles_' + str(i) + '_processed.txt', 'r') as readfile:
        with open('../../data/corpus/titles_' + str(i) + '_processed_new.txt', 'w') as writefile:
            blank = re.compile('[^ ]+')
            for line in readfile:
                line_list = line.split('.')

                for new_line in line_list:
                    if new_line.lstrip():
                        new_line_l = new_line.lstrip()
                        if new_line_l.rstrip():
                            writefile.write(' '.join(new_line_l.rstrip().split()) + '\n')
