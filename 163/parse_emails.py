#Unbuffered CSV parser

import csv
import sys
import time
from collections import OrderedDict
import pprint

csv.field_size_limit(1000000000)


def parse_csv(path):
	r = csv.reader(open(path, 'r'))
	fout = open('parse_emails_output.txt', 'w')
	# pattern = re.compile("<.+>")

	keywords = {}
	garbage_words = ['RE:', 'vacation', 'funny', 'cute', 'cute!', 'babysitting', 'watch found', 'guys night out', 'ha ha', 'casino', 'flowers', 'text and drive', 'craft night', 'coupon club', 'funy', 'borrow hedge trimmer', 'home sick', 'coffee', 'employee of the month', 'picnic', 'lottery', 'holiday', 'retirement', 'announcement', 'schedule', 'birthday', 'good morning', 'cover for me']

	for row in r:
		subject = row[3].lower()
		
		cont = False
		for word in garbage_words:
			if word in subject:
				cont = True
				break

		if cont:
			continue

		from_person = row[0].strip()
		to_people = row[1].split(',') 
		if from_person not in keywords:
			keywords[from_person] = {}
		for person_raw in to_people: #.strip
			person = person_raw.strip()
			if person in keywords[from_person]:
				keywords[from_person][person] += row[2:]
			else:
				keywords[from_person][person] = {}
				keywords[from_person][person] = row[2:]

	# fout.write(str(keywords))
	pprint.pprint(sorted(keywords.keys()))
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