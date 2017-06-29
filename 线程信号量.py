#-*- coding:UTF-8 -*-
import threading
import time

class MyThread(threading.Thread):
	def __init__(self, name):
		super(MyThread, self).__init__()
		self.name = name


	def run(self):
		semaphore.acquire()
		time.sleep(1)
		print "run {}".format(self.name)
		semaphore.release()


# 最多允许5个线程同时运行，执行完一个线程放入一个线程
semaphore = threading.BoundedSemaphore(5) 
for i in range(50):
	mt = MyThread("t-{}".format(i))
	mt.start()


while threading.active_count() != 1: # 类似于t.join()
	pass
else:
	print "all threads done"

