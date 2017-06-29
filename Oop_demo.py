#-*- coding:UTF-8 -*-

class School(object):
	def __init__(self, name, addr):
		self.name = name
		self.addr = addr

	def tell(self):
		pass


class SchoolMembers(object):
	stu_list = []
	staff_list = []


	def __init__(self, name, sex, age):
		self.name = name
		self.sex = sex
		self.age = age


	def regiester(self, obj_stu):
		print "注册学员：{}， 学号: {}".format(obj_stu.name, obj_stu.stu_id)
		self.stu_list.append(obj_stu)


	def staff(self, obj_staff):
		print "{}正在教授学生".format(obj_staff)
		self.staff_list.append(obj_staff)


class Teacher(SchoolMembers):
	def __init__(self, name, sex, age, salary, course):
		super(Teacher, self).__init__(name, sex, age)
		self.salary = salary
		self.course = course

	def tell(self):
		print "-------- Info of Teacher: {0}\
		Name: {1}\
		Age: {2}\
		Sex: {3}\
		salary: {4}\
		course: {5}".format(self.name, self.name, self.sex, self.age, self.salary, self.course)


class Student(SchoolMembers):
	def __init__(self, name, sex, age, stu_id, grade):
		super(Student, self).__init__(name, sex, age)
		self.stu_id = stu_id
		self.grade = grade

	def tell(self):
		print "-------- Info of Student: {0}\
		Name: {1}\
		Age: {2}\
		Sex: {3}\
		stu_id: {4}\
		grade: {5}".format(self.name, self.name, self.age, self.sex, self.stu_id, self.grade)

	def pay_tuition(self,amount):
		print "{}支付学费{}".format(self.name, amount)


s1 = School('育才中学', '火星')
stu = Student("张三", "M", 22, 1001, 2)
stu.tell()
stu.pay_tuition(1000)
stu.regiester(stu)
print stu.stu_list[0].name