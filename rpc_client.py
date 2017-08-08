#!/usr/bin/python
#-*- coding:UTF-8 -*-

"""
    py2是from SimpleXMLRPCServer import SimpleXMLRPCServer
    client = SimpleXMLRPCServer.xmlrpclib.ServerProxy('', allow_none=True)
"""
from xmlrpc.client import ServerPorxy
client = ServerPorxy('http://localhost:15000', allow_none=True)
rets = clinet.get('ls /tmp')
for ret in rets:
    print (ret)