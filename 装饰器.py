#-*- coding:UTF-8 -*-
import time

######### 普通的装饰器 #######################
def timer(func):
    def deco(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        stop_time = time.time()
        print "耗费时间: {}".format(start_time - stop_time)
    return deco


@timer  # test1=timeer(test1) --> test1=deco(*args, **kwargs) 
def test1(name):
    time.sleep(1)
    print "in the test1"

@timer
def test2(name, age):
    time.sleep(1)
    print "in the test2"

test1("cfq")
test2("haha", 22)
###############################################

user, passwd = 'cfq', '123456'
def auth(auth_type):  # 接受装饰器语法糖传过来的参数
    def outer(func):  # 接受被装饰函数
        def wrapper(*args, **kwargs):  # 接受被装饰函数的参数
            if auth_type == "local":
                input_user = raw_input("input uesrname: ")
                input_passwd = raw_input("input passwd: ")
                if input_user == user and input_passwd == passwd:
                    print "验证通过"
                    func(*args, **kwargs)   # 执行被装饰函数
                else:
                    print "用户名密码错误"
            elif auth_type == "ldap":
                print "搞毛ldap。。。"
                func(*args, **kwargs)
        return wrapper    # 返回
    return outer   # 还是返回


def index():
    print "in the index"

@auth(auth_type="local")
def home(*args, **kwargs):
    print "in the home"
    print "参数是：%s %s" % (args, kwargs)
    print "---------------------------------------------"

@auth(auth_type='ldap')
def manager(*args, **kwargs):
    print "in the manager"
    print "参数是：%s %s" % (args, kwargs)

index()
home('p1', 'p2', 'p3')
manager('mp1', 'mp2', 'mp3')
