#-*- coding:UTF-8 -*-
import socketserver


class MyTcpHandle(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print ("from {} recivied {}".format(self.client_address, self.data))
                self.request.send(self.data.upper())
            except ConnectionResetError as e:
                print ("客户端断开连接",e)


if __name__ == '__main__':
    HOST, PORT = 'localhost', 1024

    server = socketserver.TCPServer((HOST, PORT), MyTcpHandle)
    server.serve_forever()
