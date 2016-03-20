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

	pizzas = soup.find_all('tr')
	pizzas_splited = str(pizzas[0]).split('\n')
	sentinel = 0

	for i, element in enumerate(pizzas_splited):
		
		if 'class="pizza-nazwa"' in element:
			
			current_pizza = parse_name(i, pizzas_splited)

		elif 'class="pizza-opis"' in element:

			current_pizza = parse_ingredients(i, pizzas_splited, current_pizza)
			#print (current_pizza)
			
		elif 'class="pizza-cena"' in element:

			pizzas_procesed, sentinel = parse_prices(i, pizzas_splited, current_pizza, pizzas_procesed, sentinel)

	return pizzas_procesed


#Subfunctions of the 'parse_coloseum' function.
def parse_name(i, pizzas_splited):
	'''
	Args:
		i - index from enumerate method.
		pizzas_splited - list of lines with raw data from the menu.html page.
	
	Returns:
		current_pizza - list of all properities of pizza
						(name, spicy, ingredients, prices per size).
	'''
	if 'ostra' in pizzas_splited[i+1]:
		current_pizza = []
		temp = str(pizzas_splited[i+1])
		name = re.findall(r"[\w']+", temp)

		if name[3] == 'b':
			record = str(name[2]).strip().lstrip()
		else:
			record = ' '.join(name[2:4]).strip().lstrip()

		current_pizza.append(record)
		current_pizza.append('tak')

	else:
		current_pizza = []
		temp = str(pizzas_splited[i+1])
		name = re.findall(r"[\w']+", temp)

		if name[3] == 'b':
			record = str(name[2]).strip().lstrip()
		else:
			record = ' '.join(name[2:4]).strip().lstrip()

		current_pizza.append(record)
		current_pizza.append('nie')

	return current_pizza


def parse_ingredients(i, pizzas_splited, current_pizza):
	'''
	Args:
		i - index from enumerate method.
		pizzas_splited - list of lines with raw data from the menu.html page.
		current_pizza - list of all properties of the pizza
						(name, spicy, ingredients, prices per size).

	Returns:
		current_pizza - list of all properities of pizza
						(name, spicy, ingredients, prices per size).
	'''
	ing = []
	temp = str(pizzas_splited[i+1])
	temp2 = str(pizzas_splited[i+2])
	#temp = re.findall(r"[\w']+", temp)
	temp = re.findall(r"[\+]|[\(][\w]+|[\w]+[\)]|[\w]+[\,]|[\w]+", temp)
	temp2 = re.findall(r"[\+]|[\(][\w]+|[\w]+[\)]|[\w]+[\,]|[\w]+", temp2)

	ing.extend(temp)
	if len(temp2) > 1:
		ing.extend(temp2[1:])
	
	ingredient = []
	for element in ing:
		if element != 'br':
			ingredient.append(element)
		elif element != 'td':
			ingredient.append(element)

	ingredient = ' '.join(ingredient)
	ingredient = ingredient.split(',')
	current_pizza.extend(ingredient)

	return current_pizza


def parse_prices(i, pizzas_splited, current_pizza, pizzas_procesed, sentinel):
	'''
	Args:
		i - index from enumerate method.
		pizzas_splited - list of lines with raw data from the menu.html page.
		current_pizza - list of all properties of the pizza
						(name, spicy, ingredients, prices per size).
		pizzas_procesed - main list of the all available pizzas.
		sentinel - sentinel value for appending current pizza to all pizzas list.
							
	Returns:
		pizzas_procesed - main list of the all available pizzas.
	'''
	sentinel += 1		
	temp = str(pizzas_splited[i+1])
	temp = temp[3:8]
	current_pizza.append(temp)
	if sentinel == 3:
		final_line = ';'.join(current_pizza)
		pizzas_procesed.append(final_line)
		sentinel = 0

	return pizzas_procesed, sentinel


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
			myfile.write('{}{}'.format(str(element), '\n'))


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
# len(pizzas_splited) = 692