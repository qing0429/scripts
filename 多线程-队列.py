#-*- coding:UTF-8 -*-
import threading, time
import Queue

class Producer(threading.Thread):
	def __init__(self, name, queue):
		super(Producer, self).__init__()
		self.name = name
		self.queue = queue


	def run(self):
		while True:
			for i in range(10):
				self.queue.put('[{}] 放入骨头 [{}]'.format(self.name, i))
				time.sleep(2)


class Consumer(threading.Thread):
	def __init__(self, name, queue):
		super(Consumer, self).__init__()
		self.name = name
		self.queue = queue


	def run(self):
		while True:
			print "[{}] 抢到骨头[{}]".format(self.name, self.queue.get())



if __name__ == '__main__':
	queue = Queue.Queue(10)
	p = Producer('cfq', queue)
	c1 = Consumer('二狗子', queue)
	c2 = Consumer('三狗子', queue)

	p.start()
	c1.start()
	c2.start()
