#Email header CSV parser

import csv
import sys
import time
from collections import OrderedDict
import pprint
import operator

csv.field_size_limit(1000000000)


def parse_csv(path):
	r = csv.reader(open(path, 'r'))
	fout = open('parse_emails2_output.txt', 'w')
	# pattern = re.compile("<.+>")

	keywords = {}
	garbage_words = ['re:', 'vacation', 'funny', 'cute', 'cute!', 'babysitting', 'watch found', 'guys night out', 'ha ha', 'casino', 'flowers', 'text and drive', 'craft night', 'coupon club',
	 'funy', 'borrow hedge trimmer', 'home sick', 'coffee', 'employee of the month', 'picnic', 'lottery', 'holiday', 'retirement', 'birthday', 'good morning', 'cover for me',
	 'concert', 'testing 1 2 3', 'on my way', 'new gyro place', 'karoake', 'copier', 'out of staples', 'lunch', 'missing sweater']

	for row in r:
		subject = row[3].lower()
		
		cont = False
		for word in garbage_words:
			if word in subject:
				cont = True
				break

		if cont:
			continue

		from_person = row[0]
		to_people = row[1].split(',') 
		#now by subject
		if subject not in keywords:
			keywords[subject] = [len(to_people), 'From: ' + row[0], 'To: ' + row[1], row[2]]
		# else:
		# 	keywords[subject] += [len(to_people), 'From: ' + row[0], 'To: ' + row[1]]

		# for person_raw in to_people: #.strip
		# 	person = person_raw.strip()
		# 	if person in keywords[row[0]]:
		# 		keywords[row[0]][person] += row[2:]
		# 	else:
		# 		keywords[row[0]][person] = {}
		# 		keywords[row[0]][person] = row[2:]

	# print("starting")
	# keyword_set = set(keywords)
	# sorted_words = sorted(keyword_set, key=lambda item: int(item[0]))
	# sorted_words = sorted(keywords.items(), key=operator.itemgetter(0))
	ordered = OrderedDict(sorted(keywords.items(), key=lambda t: t[1][0]))
	pprint.pprint(ordered, fout)
	# if item[0].isdigit() else float('inf'), item))

	# fout.write(str(keywords))
	# pprint.pprint(keywords, fout)




	# monthset = set(months)
	# sorted(data, key=lambda item: (int(item.partition(' ')[0])
 #                               if item[0].isdigit() else float('inf'), item))
	# print(monthset)
	# fout.write("c#" + "-" + str(keywords['c#']) + "\n")
	# fout.write("java" + "-" + str(keywords['java']) + "\n")
	# fout.write("javascript" + "-" + str(keywords['javascript']) + "\n")
	# fout.write("php" + "-" + str(keywords['php']) + "\n")
	# fout.write("android" + "-" + str(keywords['android']) + "\n")
	# fout.write("jquery" + "-" + str(keywords['jquery']) + "\n")
	# fout.write("python" + "-" + str(keywords['python']) + "\n")
	# fout.write("c++" + "-" + str(keywords['c++']) + "\n")
	# fout.write("html" + "-" + str(keywords['html']) + "\n")
	# fout.write("mysql" + "-" + str(keywords['mysql']) + "\n")
	# fout.write("ios" + "-" + str(keywords['ios']) + "\n")
	# fout.write("asp.net" + "-" + str(keywords['asp.net']) + "\n")


	# ordered_d = OrderedDict(sorted(keywords.items(), key=lambda x: len(x[1]), reverse = True))
	# ct = 0
	# for key in ordered_d:
	# 	ct+=1
	# 	fout.write(key + "-" + str(ordered_d[key]) + "\n")
	# 	if(ct == 15):
	# 		return " "


	

parse_csv('email headers.csv')