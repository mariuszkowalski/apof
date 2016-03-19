#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import urllib.request
import re

#Addresses to parse.
URL = 'http://www.coloseum.pl/menu.html'


def main():
	raw_content = urllib.request.urlopen(URL).read()
	soup = bs(raw_content, 'lxml')
	
	'''
	#Not bad.
	for element in soup.stripped_strings:
		print(repr(element))
	'''
	pizzas = soup.find_all('tr')
	print(pizzas)

if __name__ == '__main__':
	main()

'''
<tr class="pizza-nazwa"><td colspan="4">
<b>1.&nbsp; MARGHERITA</b>
</td></tr><tr class="pizza-opis"><td>
sos podk³adowy, ser
</td>
<td class="pizza-cena" align="center">
<b>11,00</b>
</td><td class="pizza-cena" align="center">
<b>22,00</b>
</td>
<td class="pizza-cena" align="center">
<b>29,50</b>
</td></tr>
'''
