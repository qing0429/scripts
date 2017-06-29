# -*- coding:UTF-8 -*-
import multiprocessing
import time

def run(name):
	print "run task {}".format(name)
	time.sleep(2)

if __name__ == '__main__':
	for i in range(10):
		p = multiprocessing.Process(target=run, args=('进程-{}'.format(i),))
		p.start()