#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import urllib.request
import hashlib
import codecs
import os

#######################################################################################################################
#
# Settings
#
#######################################################################################################################

# Path settings.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, 'apof\parsed_sites')
SETTINGS = os.path.join(BASE_DIR, 'apof\settings')


# Addresses to parse.
URL = 'http://www.coloseum.pl/menu.html'


def read_site(url):
	raw_content = urllib.request.urlopen(url).read()
	return bs(raw_content, 'html.parser')


#######################################################################################################################
# Parse function with subfunctions.
#######################################################################################################################

def parse_coloseum(url):
	soup = read_site(url)
	
	pizzas_procesed = []

	pizzas = soup.find_all('tr')
	pizzas_splited = str(pizzas[0]).split('\n')
	sentinel = 0

	for i, element in enumerate(pizzas_splited):
		
		if 'class="pizza-nazwa"' in element:
			
			current_pizza = parse_name(i, pizzas_splited)

		elif 'class="pizza-opis"' in element:

			current_pizza = parse_ingeredients(i, pizzas_splited, current_pizza)
			#print (current_pizza)
			
		elif 'class="pizza-cena"' in element:

			pizzas_procesed, sentinel = parse_prices(i, pizzas_splited, current_pizza, pizzas_procesed, sentinel)

	return pizzas_procesed


#Subfunctions of the 'parse_coloseum' function.
def parse_name(i, pizzas_splited):
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

	return current_pizza


def parse_ingeredients(i, pizzas_splited, current_pizza):
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

	return current_pizza


def parse_prices(i, pizzas_splited, current_pizza, pizzas_procesed, sentinel):
	sentinel += 1		
	temp = str(pizzas_splited[i+1])
	temp = temp[3:8]
	current_pizza.append(temp)
	if sentinel == 3:
		final_line = ';'.join(current_pizza)
		pizzas_procesed.append(final_line)
		sentinel = 0

	return pizzas_procesed, sentinel


#######################################################################################################################
# Saveing parsed data to the file in CSV format.
#######################################################################################################################

def save_parsed(text):
	dir_1 = os.path.join(CSV_DIR, 'parsed_main')
	dir_2 = os.path.join(CSV_DIR, 'parsed_aux')
	target_1 = os.path.join(dir_1, 'coloseum_parsed.txt')
	target_2 = os.path.join(dir_2, 'coloseum_parsed.txt')

	if not os.path.exists(dir_1):
		os.makedirs(dir_1)
	if not os.path.exists(dir_2):
		os.makedirs(dir_2)

	if not os.path.isfile(target_1):
		target = target_1
	else:
		target = target_2
	
	with codecs.open(target, 'w', 'utf-8') as myfile:
		for element in text:
			myfile.write('{}{}'.format(str(element), '\n'))


#######################################################################################################################
# Compareing parsed files with data stored in the CSV format.
#######################################################################################################################

def compare_parsed():
	dir_1 = os.path.join(CSV_DIR, 'parsed_main')
	dir_2 = os.path.join(CSV_DIR, 'parsed_aux')
	target_1 = os.path.join(dir_1, 'coloseum_parsed.txt')
	target_2 = os.path.join(dir_2, 'coloseum_parsed.txt')

	is_compare_required = False

	if os.path.isfile(target_1):
		if os.path.isfile(target_2):
			is_compare_required = True

	if is_compare_required == True:
		result_from_file_1 = hashlib.sha256(codecs.open(target_1, 'rb').read()).digest()
		result_from_file_2 = hashlib.sha256(codecs.open(target_2, 'rb').read()).digest()
		print(result_from_file_1)
		print(result_from_file_2)
		if result_from_file_1 == result_from_file_2:
			print('TRUE')
		else:
			print('FALSE')


#######################################################################################################################
# Utility functions. Dismantle after the development stage.
#######################################################################################################################

def save_work_in_progres(text):
	target = os.path.join(BASE_DIR, 'apof\parsed_progres.txt')
	with codecs.open(target, 'w', 'utf-8') as myfile:
		for element in text:
			myfile.write(str(element))


#######################################################################################################################
# Main function of the script.
#######################################################################################################################

def main():
	processed_data = parse_coloseum(URL)

	#for debuging purposes only.
	#print(processed_data)
	
	#save_parsed(processed_data)
	current_data = compare_parsed()
	

if __name__ == '__main__':
	main()


######################################################################3
# len(pizzas) = 177
# len(pizzas_splited) = 692