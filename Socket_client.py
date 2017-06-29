#-*- coding:utf-8 -*-
import socket


client = socket.socket()
client.connect(('localhost', 10010))
while True:
    inp = input("# ").strip()
    if len(inp) == 0: continue
    client.send(inp.encode('UTF-8'))
    data = client.recv(1024)
    print (data)
client.close()