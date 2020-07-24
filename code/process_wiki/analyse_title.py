input_filepath = 'titles.txt'

with open(input_filepath, 'r') as readfile:
    with open('write_filepath.txt', 'w') as writefile:
        lst = {}
        for title in readfile:
            if ':' in title:
                string_list = title.split(':')
                if string_list[0] not in lst:
                    lst[string_list[0]] = 1
                else:
                    lst[string_list[0]] += 1

        sorted_lst = sorted(lst.iteritems(), key=lambda (k, v): (v, k), reverse=True)

        print sorted_lst

        for title in sorted_lst:
            print title
            writefile.write(title[0] + " " + str(title[1]) + '\n')
