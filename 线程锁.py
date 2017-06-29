#-*- coding:UTF-8 -*-
import threading
import time


def run(n):
	global num
	lock.acquire()
	num += 1
	lock.release()

num = 0
ojb_list = []
lock = threading.Lock()

for i in range(1000):
	t = threading.Thread(target=run, args=("t-{}".format(i), ))
	t.start()
	ojb_list.append(t)

for t in ojb_list:
	t.join()


print num