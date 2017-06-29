#-*- coding:UTF-8 -*-
import threading
import time


class MyThread(threading.Thread):
	def __init__(self, name):
		super(MyThread, self).__init__()
		self.name = name


	def run(self):
		print "run task {}".format(self.name)
		time.sleep(2)
		print "{} done".format(self.name)


start_time = time.time() 
t_threadlist = []

for i in range(50):
	t = MyThread("t-{}".format(i))
	t.start()
	t_threadlist.append(t)


for t in t_threadlist:
	t.join()


print "耗时: {}".format(time.time() - start_time)