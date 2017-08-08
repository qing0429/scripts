#!/usr/bin/python
#encoding=utf-8  
''''' 
 
'''  
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer  
import io,shutil    
import urllib,time  
import getopt,string  
import sys  
from src.QcloudApi.qcloudapi import QcloudApi
import logging

  
class MyRequestHandler(BaseHTTPRequestHandler):  
    def getDescribeLVBInfo(self, action, channel_id=''):
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
            rets = service.call(action, params)

            return rets
        except Exception, e:
            logging.error(e)

    def do_GET(self):
        self.process(2)
          
    def process(self, type):  
        content =""  
        if '?' in self.path:  
            query = urllib.splitquery(self.path)  
            action = query[0]  
              
            if query[1]:#接收get参数  
                queryParams = {}  
                for qp in query[1].split('&'):  
                    kv = qp.split('=')  
                    queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')  
                    logging.info("接受参数：{}".format(queryParams))
                action = queryParams['action']
                channel_id = ''
                if action == "DescribeLVBChannel":
                    channel_id = queryParams['channel_id']
                content = self.getDescribeLVBInfo(action, channel_id)
                logging.info("结果：{}".format(content))
            #指定返回编码  
            enc="UTF-8"    
            content = content.encode(enc)
            f = io.BytesIO()
            f.write(content)    
            f.seek(0)    
            self.send_response(200)    
            self.send_header("Content-type", "text/html; charset=%s" % enc)    
            self.send_header("Content-Length", str(len(content)))    
            self.end_headers()    
            shutil.copyfileobj(f,self.wfile)     
  
  
if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='/alidata1/admin/qcloud-live/logs/qcloud_live.log', filemode='a')
    if len(sys.argv)>1:  
        serverport=int(sys.argv[1])  
    else:  
        serverport=8000  
        logging.info("监听端口: {}".format(serverport))
    try:  
        server = HTTPServer(('', serverport), MyRequestHandler)  
        server.serve_forever()  
  
    except KeyboardInterrupt:  
        server.socket.close()  
    pass 