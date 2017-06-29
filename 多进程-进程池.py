# -*- coding:UTF-8 -*-
from multiprocessing import Pool, Process
import time, os


def Foo(i):
	time.sleep(1)
	print "in the process: {}".format(os.getpid())


def Bar(args):
	print "------> exec done: {}".format(os.getpid())


if __name__ == '__main__':
	print "主进程[{}]".format(os.getpid())

	pool = Pool(processes=5)
	for i in range(10):
		# pool.apply(func=Foo, args=(i,))  # 串行
		pool.apply_async(func=Foo, args=(i,), callback=Bar) # 并行  callback表示回调，执行完Foo，在执行Bar


	pool.close()  # 先close，否会出问题
	pool.join()   # 主进程不等待其他子进程的执行结果

