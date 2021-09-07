#Parses the articles in mini project 1

import csv
import sys
import time
from collections import OrderedDict
import pprint
import string
import operator
import os
import datetime
import xlsxwriter
import json
# import Set

class Person:
	def __init__(self, name, first_date):
		 self.n = name
		 self.d = first_date
	def __lt__(self, other):
		return ((self.d) <
				(other.d))
	def __eq__(self, other):
		return ((self.n.lower()) ==
				(other.n.lower()))
	def __str__(self):
		return n + ' first seen on ' + d
	def __hash__(self):
		return hash(self.n)


def main():
	fout = open('connections_output.txt', 'w')

	articles = []
	people = set()
	connections = []

	
	ct = 0
	for filename in os.listdir('articles'):
	# 	# articles.append(parse_article(filename))
		
		# ct+=1
		# if ct == 5:
		#  	break
		
		article = parse_article(filename)
		# for person1 in article[6]:
		# 	found = False
		# 	for person2 in people:
		# 		if person1 == person2:
		# 			if person1 < person2:
		# 				people.remove(person2)
		# 				people.add(person1)
		# 	if not found:
		# 		people.add(person1)

		articles.append(article)
		# connections.extend(article[7])
	# pprint.pprint(articles, fout)

	with open('jsondump.txt', 'w') as outfile:
	  json.dump(articles, outfile)
	# for person in people:
	# 	pprint.pprint(person.n + ' ' + str(person.d))

	# pprint.pprint(parse_article(filename), fout)
	# pprint.pprint("", fout)
	# pprint.pprint('/'*100, fout)
	# pprint.pprint("", fout)

	# make_xlsx(articles)
	# print(len(articles))

def parse_article(path):
	f = open('articles/'+path, 'r')
	# lines = f.readlines()

	#not used
	garbage_words = ['re:', 'vacation', 'funny', 'cute', 'cute!', 'babysitting', 'watch found', 'guys night out', 'ha ha', 'casino', 'flowers', 'text and drive', 'craft night', 'coupon club',
	 'funy', 'borrow hedge trimmer', 'home sick', 'coffee', 'employee of the month', 'picnic', 'lottery', 'holiday', 'retirement', 'birthday', 'good morning', 'cover for me',
	 'concert', 'testing 1 2 3', 'on my way', 'new gyro place', 'karoake', 'copier', 'out of staples', 'lunch', 'missing sweater']

	src = ''
	title = ''
	date = ''
	secondary_date = ''
	two_dates = False
	author = ''
	text = []

	names = ['beatriz', 'sanjorge', 'barranco', 'corrente', 'orhan', 'vasco', 'Henk','Mira','Carmine','Ale','Jeroen','Valentine','Yanick','Joreto', 'Elian','Silvia','Mandor','Isia','Julian', 'Lucio','Lorenzo']

	names_found = []
	connections = []
	people = []

	ct = 0
	for line in f:
		if line.rstrip():
			if line[0].isnumeric() and len(line) < 25:
				if date:
					date = min(date,parse_date(line.rstrip(), path))
				else:
					date = parse_date(line.rstrip(), path)
				ct+=1
				continue
			if ct == 0:
				src = line
			elif ct == 1:
				if line[0].isalpha():
					title = line
				else:
					ct+=1
			elif ct == 2:
				if line[0].isalpha() and len(line) < 25:
					author = line
			else:
				text.append(line.rstrip())
							#finding names:
				for s in names: 
					# print(s + ' ' + line)
					if s.lower() in line.lower():
						found = False
						for n in names_found:
							if s.lower() in n:
								found = True
								break
						if found == True:
							break
						# print(s)
						#                  name line found in
						names_found.append([s.lower(),    ct])
						people.append(Person(s.lower(), date))
						for other in names_found:		                   #closeness in lines
							if other[0] != s.lower():
								connections.append([s, other[0], str(date), abs(ct - other[1]), src.rstrip(), path])
			ct+=1
	if not title:
		print(path + ' has no title')

	# return([path, src.rstrip(), title.rstrip(), author.rstrip(), date, text, people, connections])
	retval = {'id': path, 'content': title.rstrip(), 'start': date.strftime('new Date(%Y, %m, %d)'), 'source': src.rstrip()}
	return retval

def parse_date(s,path):
	try:
		splitted = s.split('/')
		if len(splitted) == 3:
			return datetime.date(int(splitted[0]), int(splitted[1]), int(splitted[2]))
		
		splitted = s.split(' of ')
		if len(splitted) == 3:
			return datetime.date(int(splitted[2]), int(month_to_num(splitted[1])), int(splitted[0]))

		splitted = s.split(' ')
		if len(splitted) == 3:
			if splitted[1][0].isalpha():
				return datetime.date(int(splitted[2]), int(month_to_num(splitted[1])), int(splitted[0]))
			else:
				print(path + ' unknown: ' + s)	
		elif len(splitted) > 3:
			# for x in range(0,3):
			# 	if not splitted[x]:
			# 		splitted.remove(x)
			splitted.remove('')
			# splitted.remove(' ')
			if splitted[1][0].isalpha():
				return datetime.date(int(splitted[2]), int(month_to_num(splitted[1])), int(splitted[0]))
		elif len(splitted) == 2:
			if splitted[0][2].isalpha() and splitted[0][1].isnumeric():
				return datetime.date(int(splitted[1]), int(month_to_num(splitted[0][2:])), int(splitted[0][0:2]))
		
		else:
			print(path + ' unknown: ' + s)

	except TypeError as e:
		print(s,path)
		raise e

def month_to_num(month):
	return{
			'Jan' : 1,
			'January' : 1,
			'Feb' : 2,
			'February' : 2,
			'Mar' : 3,
			'March' : 3,
			'Apr' : 4,
			'April' : 4,
			'May' : 5,
			'Jun' : 6,
			'June' : 6,
			'Jul' : 7,
			'July' : 7,
			'Aug' : 8,
			'August' : 8,
			'Sep' : 9, 
			'September' : 9, 
			'Oct' : 10,
			'October' : 10,
			'Nov' : 11,
			'November' : 11,
			'Dec' : 12,
			'December' : 12
	}[month]


def make_xlsx(articles):
	
	# Create an new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook('vast timeline.xlsx')
	worksheet = workbook.add_worksheet()

	# Widen the first column to make the text clearer.
	worksheet.set_column('A:A', 20)
	worksheet.set_column('F:F', 12)
	worksheet.set_column('G:G', 16)
	worksheet.set_column('H:H', 16)

	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': True})
	dateformat = workbook.add_format({'num_format': 'mm/dd/yyyy h:mm:ss'})
	

	#Headers
	worksheet.write('A1', 'Start Date', bold)
	worksheet.write('B1', 'End Date', bold)
	worksheet.write('C1', 'Headline', bold)
	worksheet.write('D1', 'Text', bold)
	worksheet.write('E1', 'Media', bold)
	worksheet.write('F1', 'Media Credit', bold)
	worksheet.write('G1', 'Media Caption', bold)
	worksheet.write('H1', 'Media Thumbnail', bold)
	worksheet.write('I1', 'Type', bold)
	worksheet.write('J1', 'Tag', bold)

	# for article in arcticles
	# Write some numbers, with row/column notation.
	row = 1
	for article in articles:#lets write 
		worksheet.write_datetime(row, 0, article[4][0], dateformat) #date
		# worksheet.write(row, 0, number, format5)       # 28/02/13 12:00
		worksheet.write(row, 2, article[2]) #Headline
		worksheet.write(row, 4, "\n\n".join(article[5][0:2])) #text
		worksheet.write(row, 6, article[3]) #author?
		worksheet.write(row, 6, article[1]) #source?
		row += 1
		# if row == 10:
		# 	break
		

	#[path, src.rstrip(), title.rstrip(), author.rstrip(), date, text]

	workbook.close()


main()
# with open('connections_output.txt') as inf, open('conections_formatted',"w") as outf:
#     # line_words = line for line in inf
#     # outf.writelines(words for words in line_words if len(words)>1)

#     for l in inf:
#     	line = l.replace('\'', '').replace('[', '').replace(']', '')
#     	# line = line[:-1]
#     	outf.write(line)