#-*- coding: utf-8 -*-
#맨 처음 25GB -> 3GB (MBER_SEQ가 없는 거 짜름)
filepath = '20160701~20160930.json'

with open('json.txt', 'w') as writefile:
	with open(filepath) as readfile:
		for i, line in enumerate(readfile):
			if(i < 3):
				continue
			checkString = line[line.find('"MBER_SEQ"'):line.find(',', line.find('"MBER_SEQ"'))]
			if(checkString == '"MBER_SEQ" : "-"'):
				continue

			else:
				jsonString = "{ " + line[line.find('"uri"'):line.find(',', line.find('"uri"'))] + ", "
				jsonString += line[line.find('"referer"'):line.find(',', line.find('"referer"'))] + ", "

				if(line.find('"new_query_string"') == -1):
					jsonString += line[line.find('"MBER_SEQ"'):line.find(',', line.find('"MBER_SEQ"'))] + " }\n"
				else:
					jsonString += line[line.find('"MBER_SEQ"'):line.find(',', line.find('"MBER_SEQ"'))] + ", "
					jsonString += line[line.find('"new_query_string"'):]

				writefile.write(jsonString)