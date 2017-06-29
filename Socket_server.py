#-*- coding:utf-8 -*-
import socket


server = socket.socket()
server.bind(('localhost', 10010))
server.listen(1)
conn, addr = server.accept()

while True:
    print ("等待接收消息")
    data = conn.recv(1024)
    print ("消息来了")
    print (data)
    conn.send(data.upper())
server.close()