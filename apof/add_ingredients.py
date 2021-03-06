#!/usr/bin/env Python3
# -*- coding: utf-8 -*-

#Read the settings file and initialize the django db.
import os
from django import setup as django_setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apof.settings.common")
django_setup()

#Read models from restaurants models and settings from parse_coloseum.
from restaurants.models import Restaurant, Meal, Ingredients
from parse_coloseum import BASE_DIR, CSV_DIR, URL
from parse_coloseum import read_site
from parse_coloseum import parse_coloseum, parse_name, parse_ingredients, parse_prices
from parse_coloseum import save_parsed, compare_parsed
import codecs
import csv
import time


TARGET_DIR = os.path.join(CSV_DIR, 'parsed_main\coloseum_parsed.txt')


def open_file():
	all_pizzas = []
	
	if not os.path.isfile(TARGET_DIR):
		print('Primary check failed.')
		procesed_data = parse_coloseum(URL)
		save_parsed(procesed_data)
		compare_parsed()
	else:
		print('Primary check succeded.')
	
	try:
		current_file = codecs.open(TARGET_DIR, 'r', 'utf-8')
	
	except FileNotFoundError:
		print('Running through exception. Something went totaly wrong.')

	else:
		print('Running througn normal mode of operations.')
		data = csv.reader(current_file, delimiter=';')
		
		for row in data:
			all_pizzas.append(row)
		current_file.close()
		
		return all_pizzas


def populate(alist):
	for element in alist:
		i1 = Ingredients(ingredient_name=element)
		i1.save()

def main():
	data = open_file()
	'''
	all_ingredients = set()
	
	for element in data:
		for ingredient in (element[2:-3]):
			all_ingredients.add(ingredient)

	all_ingredients = list(all_ingredients)
	print(all_ingredients)
	'''
	print(data)
	print('Everything went ok.')
	#populate(ingredients)


if __name__ == '__main__':
	main()
