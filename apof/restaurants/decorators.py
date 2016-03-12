import json


def parse_json(func):

	def parse(self, request, *args, **kwargs):
		request.data = json.loads(request.read())
		return func(self, request, *args, **kwargs)

	return parse


def italic(func):
	
	def inner(alist):
		for i, element in enumerate(alist):
			if not isinstance(element, str):
				raise Exception('A non string was encountered.')
			 alist[i] = '<i>{}</i>'.format(element)
		return func(alist)
	
	return inner


def bold(func):
	
	def inner(alist):
		for i, element in enumerate(alist):
			if not isinstance(element, str):
				raise Exception('A non string was encountered.')
			 alist[i] = '<b>{}</b>'.format(element)
		return func(alist)
	
	return inner


