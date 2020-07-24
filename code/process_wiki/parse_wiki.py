import xml.etree.ElementTree as ETree

input_filepath = '../data/kowiki.xml'
# doc = ETree.parse(input_filepath)
# root = doc.getroot()

page_count = 0
with open('titles_0.txt', 'w') as writefile_0:
    with open('titles_1.txt', 'w') as writefile_1:
        with open('titles_2.txt', 'w') as writefile_2:
            with open('titles_3.txt', 'w') as writefile_3:
                with open('titles_4.txt', 'w') as writefile_4:
                    count = 0
                    for event, elem in ETree.iterparse(input_filepath, events=('start', 'end')):
                        if event == 'start':
                            if elem.tag.endswith('text'):
                                if elem.text is not None:
                                    count += 1
                                    if count % 5 == 0:
                                        writefile_0.write(str(elem.text.encode('utf-8') + '\n'))
                                    if count % 5 == 1:
                                        writefile_1.write(str(elem.text.encode('utf-8') + '\n'))
                                    if count % 5 == 2:
                                        writefile_2.write(str(elem.text.encode('utf-8') + '\n'))
                                    if count % 5 == 3:
                                        writefile_3.write(str(elem.text.encode('utf-8') + '\n'))
                                    if count % 5 == 4:
                                        writefile_4.write(str(elem.text.encode('utf-8') + '\n'))
        #         if elem.text is not None:
        #             writefile.write(elem.text.encode('utf-8') + '\n')
        #             page_count += 1
        # elif event == 'end':
        #     if elem.tag.endswith('title'):
        #         print elem.text
        #         break
    elem.clear()
