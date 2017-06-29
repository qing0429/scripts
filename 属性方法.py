# -*- coding:UTF-8 -*-

class Flight(object):
	__status = 0


	def __init__(self, name):
		self.flight_name = name


	def check_flight_status(self):
		print "check {} status".format(self.flight_name)
		return self.__status


	@property
	def flight_status(self):
		status = self.check_flight_status()
		if status == 0:
			print "flight status：cancle"
		elif status == 1:
			print "flight status: delay"
		elif status == 2:
			print "flight status: departure"
		else:
			print "can not get flight stauts"


	@flight_status.setter
	def flight_status(self, status):
		print "change flight status to {}".format(status)
		self.__status = status


f = Flight('CA930')
f.flight_status
f.flight_status = 2
f.flight_status