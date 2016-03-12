def italic(func):
	
	def inner(alist):
		for i, element in enumerate(alist):
			if not isinstance(element, str):
				raise Exception('A non string was encountered.')
			alist[i] = '<i>{}</i>'.format(element)
		return func(alist)
	
	return inner

@italic
def test(alist):
	return alist

def main():
	text = ['aaaaaa', 'bbbbbb']
	print(test(text))


if __name__ == '__main__':
	main()
	
