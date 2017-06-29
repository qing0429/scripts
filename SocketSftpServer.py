# -*- coding:UTF-8 -*-
import socket, os, hashlib

server = socket.socket()
server.bind(('10.139.96.117', 1024))
server.listen(1)
conn, addr = server.accept()
while True:
    print "准备开始接受数据"
    data = conn.recv(1024)
    if not data:
        print "客户端已经断开连接"
        break
        
    if os.path.isfile(data):
        file_size = os.stat(data).st_size
        conn.send(str(file_size))
        f = open(data, 'rb')
        m = hashlib.md5()
        for line in f:
            m.update(line)
            conn.send(line)

        f.close()
        conn.send(m.hexdigest())
