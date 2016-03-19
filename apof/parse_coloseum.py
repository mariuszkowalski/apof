#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import urllib.request
import codecs
import os


#Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, 'apof\parsed_sites')
SETTINGS = os.path.join(BASE_DIR, 'apof\settings')

#Addresses to parse.
URL = 'http://www.coloseum.pl/menu.html'


def read_site(address):
	raw_content = urllib.request.urlopen(address).read()
	return bs(raw_content, 'html.parser')


def save_work_in_progres(text):
	target = os.path.join(BASE_DIR, 'apof\parsed_progres.txt')
	with codecs.open(target, 'w', 'utf-8') as myfile:
		for element in text:
			myfile.write(str(element))


def save_parsed(text):
	target = os.path.join(BASE_DIR, 'apof\parsed.txt')
	with codecs.open(target, 'w', 'utf-8') as myfile:
		for element in text:
			myfile.write('{}{}'.format(str(element), '\n'))


def main():
	soup = read_site(URL)
	pizzas_procesed = []

	pizzas = soup.find_all('tr')
	pizzas_splited = str(pizzas[0]).split('\n')
	sentinel = 0

	for i, element in enumerate(pizzas_splited):
		
		if 'class="pizza-nazwa"' in element:
			
			if 'ostra' in pizzas_splited[i+1]:
				current_pizza = []
				temp = str(pizzas_splited[i+1])
				temp = temp[7:-39].strip().lstrip()
				current_pizza.append(temp)
				current_pizza.append('tak')

			else:
				current_pizza = []
				temp = str(pizzas_splited[i+1])
				temp = temp[7:-4].strip().lstrip()
				current_pizza.append(temp)
				current_pizza.append('nie')
		
		elif 'class="pizza-opis"' in element:
			temp = str(pizzas_splited[i+1])
			temp = temp.split(',')
			for nr, ingr in enumerate(temp):
				if '<br>' in ingr:
					subprocess = str(ingr).split('<br>')
					temp[nr] = ''.join(subprocess).strip().lstrip()
					current_pizza.append(temp[nr])
				else:
					temp[nr] = str(ingr).strip().lstrip()
					current_pizza.append(temp[nr])
		
		elif 'class="pizza-cena"' in element:
			sentinel += 1		
			temp = str(pizzas_splited[i+1])
			temp = temp[3:8]
			current_pizza.append(temp)
			if sentinel == 3:
				final_line = ';'.join(current_pizza)
				pizzas_procesed.append(final_line)
				sentinel = 0


	print(pizzas_procesed)
	save_parsed(pizzas_procesed)
	

if __name__ == '__main__':
	main()


######################################################################3
# len(pizzas) = 177
# len(pizzas_splited) = 692