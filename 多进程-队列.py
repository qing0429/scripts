# -*- coding:UTF-8 -*-
from multiprocessing import Process, Queue


def run(qq):
	qq.put([11, None, 'hello'])


if __name__ == '__main__':
	q = Queue()
	p = Process(target=run, args=(q,))
	p.start()

	st = q.get()
	print st
	p.join()