#!/usr/bin/python
#-*- coding:UTF-8 -*-
#接收域名和对应ip，修改dns配置文件重新解析域名
import socketserver
import logging
import json
import datetime
import shutil
import re
import subprocess


def update_config(domain, ip):
    #备份DNS配置文件
    shutil.copy(CONFIG_PATH, CONFIG_BAK_PATH)
    with open(CONFIG_PATH, 'r') as f, open(TMP_CONFIG, 'w+') as tf:
        for line in f:
            match = re.search('\d+.\d+.\d+.\d+'.format(), line)  # 匹配域名解析内容
            if match:
                L_domain, L_flag, L_record, L_ip = line.split()
                match = re.match('{}$'.format(domain), L_domain)  # 匹配接收到的域名是否被解析过
                if match:
                    line = "{}        IN A        {}".format(domain, ip)
                    logging.warn("域名{}之前被解析到{}, 现在重新解析为{}".format(domain, L_ip, ip))
                else:
                    line = "{}        IN A        {}".format(domain, ip)
                    logging.info("域名{}已经解析到{}".format(domain, ip))
            tf.write(line)


def check_config(domain, ip, rets):
    rets = rets
    with open(CONFIG_PATH) as f:
        for line in f:
            match = re.search('\d+.\d+.\d+.\d+', line)
            if match:
                L_domain, L_flag, L_record, L_ip = line.split()
                if L_domain == domain and L_ip == ip:
                    logging.info("{}解析到{}完成".format(L_domain, L_ip))
                    status = subprocess.Popen('systemctl restart named', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    if status == 0:
                        logging.info("重启named完成")
                        rets['status'] = "success"
                    else:
                        logging.error("重启named失败")
                        rets['status'] = "failed"
                else:
                    logging.error("{}解析到{}失败".format(L_domain, L_ip))
                    rets['status'] = "failed"
    return rets


class TcpHandler(socketserver.BaseRequestHandler):
    """

    """
    def handle(self):
        while True:
            try:
                self.rets = {}
                self.recv_data = self.request.recv(1024).strip()
                if len(self.recv_data) == 0:break
                logging.info("from {} recivied {}".format(self.client_address, self.recv_data))
                self.data = json.loads(self.recv_data)
                if 'domain' in self.data.keys() and 'ip' in self.data.keys():
                    self.domain = self.data['domain']
                    self.ip = self.data['ip']
                    update_config(self.domain, self.ip)
                    self.rets = check_config(self.domain, self.ip, self.rets)
                else:
                    logging.error("接受到的参数有错误{}".format(self.recv_data))
                    self.rets['status'] = 'failed'
                self.rets = json.dumps(self.rets)
                self.request.send(self.rets.encode())
            except ConnectionResetError as e:
                logging.error("客户端断开连接",e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='/var/log/domain_reslove.log', filemode='a')
    DATE = datetime.datetime.now().strftime('%Y%m%d')
    HOST, PORT = '0.0.0.0', 1024
    # CONFIG_PATH = '/var/named/chroot/var/named/za-tech.net.zone'
    # CONFIG_PATH = '/var/named/chroot/var/named/za-tech.net.zone.tmp'
    # CONFIG_BAK_PATH = '/var/named/chroot/var/named/za-tech.net.zone.{}'.format(DATE)
    CONFIG_PATH = '/root/named/za-tech.net.zone'
    TMP_CONFIG = '/root/named/za-tech.net.zone.tmp'
    CONFIG_BAK_PATH = '/root/named/za-tech.net.zone.{}'.format(DATE)
    server = socketserver.TCPServer((HOST, PORT), TcpHandler)
    server.serve_forever()