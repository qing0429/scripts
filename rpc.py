#!/usr/bin/python
#-*- coding:UTF-8 -*-

"""
    py2是from SimpleXMLRPCServer import SimpleXMLRPCServer
"""

from xmlrpc.server import SimpleXMLRPCServer
import subprocess

class HandlerServer():
    _rpc_methods_ = ['get']
    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for m in self._rpc_methods_:
            self._serv.register_function(getattr(self, m))

    def get(self, cmd):
        rets = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return rets.communicate()

    def serve_forever(self):
        self._serv.serve_forever()


if __name__ == '__main__':
    hserver = HandlerServer(('', 15000))
    hserver.serve_forever()



