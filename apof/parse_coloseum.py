#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from shutil import copyfile
import urllib.request
import hashlib
import codecs
import os
import re

#----------------------------------------------------------------------------------------------------------------------
# Settings
#----------------------------------------------------------------------------------------------------------------------

# Path settings.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, 'apof\parsed_sites')
SETTINGS = os.path.join(BASE_DIR, 'apof\settings')


# Addresses to parse.
URL = 'http://www.coloseum.pl/menu.html'

#State of debug mode.
DEBUG = False


def read_site(url):
	raw_content = urllib.request.urlopen(url).read()
	return bs(raw_content, 'html.parser')


#----------------------------------------------------------------------------------------------------------------------
# Parse function with subfunctions.
#----------------------------------------------------------------------------------------------------------------------

def parse_coloseum(url):
	'''
	Parses the Coloseum menu.html.

	Returns:
		list: pizzas_procesed - contains list of all current pizzas from the menu.
	'''
	soup = read_site(url)

	pizzas_procesed = []
	#current_pizza = []

	pizzas = soup.find_all('tr')
	all_names = pizzas[0].find_all('tr', {'class': 'pizza-nazwa'})
	all_properties = pizzas[0].find_all('tr', {'class': 'pizza-opis'})
	all_prices = pizzas[0].find_all('td', {'class': 'pizza-cena'})
	
	#49 pizzas
	for item in all_names:
		current_pizza = parse_name(item)
		pizzas_procesed.append(current_pizza)

	for i, item in enumerate(all_properties):
		current_pizza = parse_ingredients(item)
		
		for element in current_pizza:
			pizzas_procesed[i].append(element)
		

	current_pizza = []
	main_index = 0
	for i, item in enumerate(all_prices):
		current_price = parse_prices(item)
		current_pizza.append(current_price)
		if len(current_pizza) == 3:
			for price in current_pizza:
				pizzas_procesed[main_index].append(price)
			current_pizza = []
			main_index += 1
		#pizzas_procesed[i].append(element)

	return pizzas_procesed


#Subfunctions of the 'parse_coloseum' function.
def parse_name(current_name_processed):

	current_pizza = []
	name_build = []
	spicy_check = False
	
	name_raw = str(current_name_processed.get_text())
	name_elements = re.findall(r"[\w]+", name_raw)
	
	for element in name_elements[1:]:
		if element != 'ostra':
			name_build.append(element)
		
		if element == 'ostra':
			spicy_check = True

	name = ' '.join(name_build)
	current_pizza.append(name)

	if spicy_check == True:
		current_pizza.append('tak')
	
	else:
		current_pizza.append('nie')	

	return current_pizza


def parse_ingredients(current_properties_parsed):
	current_pizza = []
	properties_build = []

	properties_raw = current_properties_parsed.find_all('td')
	properties = str(properties_raw[0].get_text())
	properties_elements = properties.replace('\n',',').split(',')
	
	for element in properties_elements:
		element_ready_to_write = str(element).lstrip().strip()
		if len(element_ready_to_write) != 0:
			current_pizza.append(element_ready_to_write)
	
	return current_pizza


def parse_prices(current_price_parsed):
	price_raw = current_price_parsed.find_all('b')
	price = str(price_raw[0].get_text())
	
	return price
	



#----------------------------------------------------------------------------------------------------------------------
# Saveing parsed data to the file in CSV format.
#----------------------------------------------------------------------------------------------------------------------

def save_parsed(a_list):
	'''
	Saves parsed data to file in CSV format.
	If data file is present in main directory,
	creates file in aux directory.
	'''
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
		for element in a_list:
			element_ready_to_write = ';'.join(element)
			myfile.write('{}{}'.format(str(element_ready_to_write), '\n'))


#----------------------------------------------------------------------------------------------------------------------
# Compareing parsed files with data stored in the CSV format.
#----------------------------------------------------------------------------------------------------------------------

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
		result_from_file_1 = hashlib.sha256(open(target_1, 'rb').read()).digest()
		result_from_file_2 = hashlib.sha256(open(target_2, 'rb').read()).digest()
		if result_from_file_1 == result_from_file_2:
			print('TRUE')
			os.remove(target_2)
		else:
			print('FALSE')
			copyfile(target_2, target_1)
			os.remove(target_2)


#----------------------------------------------------------------------------------------------------------------------
# Utility functions. Dismantle after the development stage.
#----------------------------------------------------------------------------------------------------------------------

def save_work_in_progres(a_list):
	target = os.path.join(BASE_DIR, 'apof\parsed_progres.txt')
	with codecs.open(target, 'w', 'utf-8') as myfile:
		for element in a_list:
			myfile.write(str(element))


#----------------------------------------------------------------------------------------------------------------------
# Main function of the script.
#----------------------------------------------------------------------------------------------------------------------

def main():
	if DEBUG == False:
		processed_data = parse_coloseum(URL)
		save_parsed(processed_data)
		compare_parsed()
	
	elif DEBUG == True:
		bs = read_site(URL)
		save_work_in_progres(bs)


if __name__ == '__main__':
	main()


######################################################################
# Disregard that, those are only my notes.
# len(pizzas) = 177
# len(current_pizza) = 692