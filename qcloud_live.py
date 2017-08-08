#!/usr/bin/python
# -*- coding: utf-8 -*-
import SocketServer
import logging
import datetime, re
import json
from src.QcloudApi.qcloudapi import QcloudApi

def getDescribeLVBInfo(action, channel_id=''):
    logging.info('开始查询')
    module = 'live'
    action = action
    config = {
        'Region': 'shanghai',
        'secretId': '你的id',
        'secretKey': '你的key',
        'method': 'post'
    }
    # 获取频道详情需要指定channel_id
    if channel_id == '':
        params = {
            'SignatureMethod':'HmacSHA1',#指定所要用的签名算法，可选HmacSHA256或HmacSHA1，默认为HmacSHA1
        }
    else:
        params = {
            'channelId':'{}'.format(channel_id),
            'SignatureMethod':'HmacSHA1',
        }

    try:
        service = QcloudApi(module, config)
        logging.info(service.generateUrl(action, params))
        rets = service.call(action, params)
        logging.info("请求结果: {}".format(rets))

        return rets
    except Exception, e:
        logging.info(e)


class TcpHandler(SocketServer.BaseRequestHandler):
    """
    接受socket连接，获取直播列表和直播频道详情
    """
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024).strip()
                if len(data) == 0:break   # 接收的数据长度为0是，断开本次连接
                logging.info("from {} recivied {}".format(self.client_address, data))
                # data = json.loads(data.decode()) # 接收到json类型数据，转换为python字典类型
                if 'GET' in data:
                    tmp = data.split('\n')[0]  # tmp = 'GET /?action=DescribeLVBChannel&channel_id=9896587163808546199 HTTP/1.1'
                    data = {}
                    data['action'] = re.split(' |\?|&|=', tmp)[3]
                    if data['action'] = "DescribeLVBChannel":
                        data['channel_id'] = re.split(' |\?|&|=', tmp)[5]
                else:
                    data = json.loads(data.decode()) # 接收到json类型数据，转换为python字典类型
                action = data['action']
                channel_id = ''
                if action == 'DescribeLVBChannel':
                    channel_id = data['channel_id']
                # 获取频道信息    
                rets = getDescribeLVBInfo(action, channel_id)
                self.request.sendall(rets) # 返回给客户端json类型的数据，以UTF-8形式编码
                logging.info('返回值：{}'.format(rets))
            except Exception,e:
                logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='/var/log/qcloud_live.log', filemode='a')
    DATE = datetime.datetime.now().strftime('%Y%m%d')
    HOST, PORT = '0.0.0.0', 1024
    server = SocketServer.TCPServer((HOST, PORT), TcpHandler)
    server.serve_forever()