#!/usr/bin/env Python
# -*- coding: utf-8 -*-
from django.db import models
from restaurants.models import Restaurant, Meal, Ingredients

ingredients = ['sos podkładowy',
			   'ser',
			   'szynka',
			   'pieczarki',
			   'boczek',
			   'cebula',
			   'kurczak',
			   'salami',
			   'papryka',
			   'oliwki',
			   'tuńczyk',
			   'kukurydza',
			   'krewetki',
			   'czosnek',
			   'pepperoni',
			   'tabasco',
			   'ananas',
			   'mięso mielone',
			   'pomidor',
			   'mięso kebab',
			   'małże',
			   'ogórek świeży',
			   'ser feta',
			   'kapary',
			   'ser pleśniowy',
			   'kiełbasa żywiecka',
			   'ogórek konserwowy',
			   'szpinak',
			   'jajko',
			   'gouda',
			   'lazur',
			   'brie',
			   'sos boloński',
			   'groszek',
			   'brokuły',
			   'ziarno słonecznika',
			   'rukola',
			   'suszone pomidory',
			   'szparagi',
			   'polędwica',
			   'banan',
			   'anchois',
			   'ogórek',
			   'kabanos',
			   'ser favita',
			   'kurki',
			   'przyprawy',
			   'ser pleśniowy',
			   'mozzarella',
			   'świeża rucola',
			   'szynka parmeńska']


def populate(alist):
	for element in alist:
		i1 = Ingredients(ingredient_name=element)
		i1.save()

def main():
	populate(ingredients)


if __name__ == '__main__':
	main()