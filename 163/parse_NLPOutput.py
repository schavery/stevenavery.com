#Unbuffered CSV parser

import sys
from collections import OrderedDict
import pprint
import string
import operator
import os
import re
import json

# This script is to map filenames to related people's names

# get value by tag
def getValue(buf): # buf is curren line, str is the tag
	return re.sub('<.*?>','', buf).strip()

# A typical token
# <token id="1">
#             <word>The</word>
#             <lemma>the</lemma>
#             <CharacterOffsetBegin>0</CharacterOffsetBegin>
#             <CharacterOffsetEnd>3</CharacterOffsetEnd>
#             <POS>DT</POS>
#             <NER>O</NER>
#             <Speaker>PER0</Speaker>
# </token>
 
def parse_xml(path):
	f = open('nlpxmloutput/'+str(path)+".xml", 'r')
	personName = [] 
	organization = []
	location = []
	dates = []
	dumDate = [#'XXXX-WXX-1','XXXX-WXX-2','XXXX-WXX-3','XXXX-WXX-4','XXXX-WXX-5', 'XXXX-WXX-6','XXXX-WXX-7',
				'XXXX-WXX-*'
				'THIS P1D','OFFSET P-3Y INTERSECT THIS P1D',
				]
	for l in f:
		if '<token' in l:
			Word = f.next()
			Lemma = f.next()
			f.next() 	#offsetBegin
			f.next()	#offsetEnd
			f.next()	#POS
			Ner = f.next()
			ner =  getValue(l)				
			if 'GAStech' in getValue(Word) and 'GAStech' not in organization:
				organization.append(getValue(Word))
			if 'POK' in getValue(Word) and 'POK' not in organization:
				organization.append(getValue(Word))
			if 'Protectors' in getValue(Word) and 'Protectors' not in organization:
				organization.append(getValue(Word))
			elif 'PERSON' in Ner:
				name = getValue(Word)
				if name not in personName:
					personName.append(name)
			elif 'LOCATION' in Ner:
				loc = getValue(Word)
				if loc not in location:
					location.append(loc)
			elif 'ORGANIZATION' in Ner:
				org = getValue(Word)
				if org not in organization:
					organization.append(org)
			elif 'DATE' in Ner:
				Ner_norm = f.next()
				date = getValue(Ner_norm)
				if not any(c.isalpha() for c in date):
					dates.append(date)
	info = {'file': path, 
			'person': personName,
			'organization': organization, 
			'location': location,
			'date': dates}
	return info

def main():
	fout = open('PLO_articles.txt', 'w')

	sources = {}
	articles = []
	
	ct = 0
	for filename in os.listdir('nlpxmloutput'):
		#print filename
		pprint.pprint(parse_xml(ct), fout)
		ct+=1

main()
