#-*- coding:UTF-8 -*-

def fib(max):
	n, a, b = 0, 0, 1
	while n < max:
		yield b
		a, b = b, a + b
	 	n = n + 1

f = fib(10)

while True:
	try:
		g = next(f)
		print g
	except StopIteration, e:
		print e
		break
