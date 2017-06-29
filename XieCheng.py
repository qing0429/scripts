#-*- coding:utf啊、-8 -*-
import time, sys

print sys.stdin.encoding
print sys.stdout.encoding
def consumer(name):
	print "{} 准备吃包子了".format(name)
	while True:
		baozi = yield
		print "包子{}来了， 包子被{}吃了".format(baozi, name)

def producer(name):
	c1 = consumer('A')
	c2 = consumer('B')

	c1.next()
	c2.next()

	print u"猴哥开始吃包子了"
	for i in range(10):
		time.sleep(1)
		print u"做了俩包子出来"
		c1.send(i)
		c2.send(i)


producer('cfq')
