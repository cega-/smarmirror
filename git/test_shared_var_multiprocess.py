#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Manager
from time import sleep

def f1(d, l):
	i = 0
	while True:
		d[i] = 'Super fort {0}'.format(i)
		sleep(1)
		i += 1

def f2(d, l):
	while True:
		if len(d):
			print(d)
		sleep(3)

if __name__ == '__main__':
	manager = Manager()
	d = manager.dict()
	l = manager.list(range(10))

	p1 = Process(target=f1, args=(d, l))
	p2 = Process(target=f2, args=(d, l))
	p1.start()
	p2.start()
	p1.join()
	p2.join()
		