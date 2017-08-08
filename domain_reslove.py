#!/usr/bin/python
#-*- coding:UTF-8 -*-
#接收域名和对应ip，修改dns配置文件重新解析域名
import socketserver
import logging
import json
import datetime
import shutil
import re, os
import subprocess


def update_config(domain, ip):
    """
    1. 备份域名
    2. 检查域名之前是否被解析过，并做相应的处理
    """
    shutil.copy(CONFIG_PATH, CONFIG_BAK_PATH)#备份DNS配置文件
    logging.info("开始修改配置文件，domain={}, ip={}".format(domain, ip))
    with open(CONFIG_PATH, 'r') as f, open(TMP_CONFIG_PATH, 'w+') as tf:
        is_match = 'N'  # 记录是否匹配到以前解析过的域名
        for line in f:
            match = re.search('\d+.\d+.\d+.\d+'.format(), line)  # 匹配域名解析内容
            if match:
                L_domain, L_flag, L_record, L_ip = line.split()
                match = re.match('{}$'.format(domain), L_domain)  # 匹配接收到的域名是否被解析过
                if match:
                    is_match = 'Y'
                    line = "{}        IN A        {}".format(domain, ip)  # 域名以前被即解析过，重新解析
                    logging.warn("域名{}之前被解析到{}, 现在重新解析为{}".format(domain, L_ip, ip))
                else:
                    is_match = 'N'
            tf.write(line)
        # 域名以前没有解析过    
        if is_match == "N":
            line = "{}        IN A        {}".format(domain, ip)
            logging.info("域名{}已经解析到{}".format(domain, ip))
            tf.write(line + '\n')

        shutil.move(TMP_CONFIG_PATH, CONFIG_PATH)
        logging.info("DNS配置文件修改完成")


def check_config(domain, ip):
    """
    检查域名配置是否成功，并返回json类型的结果
    """
    rets = {}
    is_success = "N"
    logging.info("检查修改结果")
    with open(CONFIG_PATH) as f:
        for line in f:
            match = re.search('\d+.\d+.\d+.\d+', line)
            if match:
                L_domain, L_flag, L_record, L_ip = line.split()  # 格式 abc.123.abc IN A 10.10.10.10
                if L_domain == domain and L_ip == ip:
                    logging.info("{}解析到{}完成".format(L_domain, L_ip))
                    status = subprocess.Popen('systemctl restart named', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    err_mesg_len = len(status.stderr.readlines())
                    if err_mesg_len == 0:
                        is_success = "Y"
                        logging.info("重启named完成")
                        rets['status'] = "success"
                        rets['comments'] = '{} - {} reslove finished'.format(L_domain, L_ip)
                    else:
                        is_success = "N"
                        rets['status'] = "failed"
                        rets['comments'] = 'restart named failed'
                        logging.error("重启named失败, {}解析到{}操作未完成".format(L_domain, L_ip))                       
        if is_success == "N":  # 没有配上或者重启named服务失败，记录日志，设置status最后的值
            logging.error("{}解析到{}失败".format(domain, ip))
            rets['status'] = "failed"
    return json.dumps(rets)


class TcpHandler(socketserver.BaseRequestHandler):
    """
    1. 创建socket进程
    2. 调用 update_config() 方法来修改named配置文件
    3. 调用 check_config() 方法来获取配置结果
    """
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                if len(self.data) == 0:break   # 接收的数据长度为0是，断开本次连接
                logging.info("from {} recivied {}".format(self.client_address, self.data))
                self.data = json.loads(self.data.decode()) # 接收到json类型数据，转换为python字典类型
                if 'domain' in self.data.keys() and 'ip' in self.data.keys(): # 判断接收的数据是否符合要求
                    self.domain = self.data['domain']
                    self.domain = self.domain.split('.test.za-tech')[0]   # 取出.za-tech前边的部分
                    self.ip = self.data['ip']
                    update_config(self.domain, self.ip)  # 调用方法修改配置文件
                    self.rets = check_config(self.domain, self.ip)  # 获取修改配置文件操作的结果
                else:
                    logging.error("接受到的参数有错误{}".format(self.data))
                    self.rets['status'] = 'failed'
                self.request.send(self.rets.encode()) # 返回给客户端json类型的数据，以UTF-8形式编码
                logging.info('返回值：{}'.format(self.rets))
            except ConnectionResetError as e:
                logging.error("客户端断开连接",e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='/var/log/domain_reslove.log', filemode='a')
    DATE = datetime.datetime.now().strftime('%Y%m%d')
    HOST, PORT = '0.0.0.0', 1024
    CONFIG_HOME = '/var/named/chroot/var/named'
    CONFIG_PATH = os.path.join(CONFIG_HOME, 'za-tech.net.zone')
    TMP_CONFIG_PATH = os.path.join(CONFIG_HOME, 'za-tech.net.zone.tmp')
    CONFIG_BAK_PATH = os.path.join(CONFIG_HOME, 'backup', 'za-tech.net.zone.{}'.format(DATE))
    # CONFIG_PATH = '/root/named/za-tech.net.zone'
    # TMP_CONFIG_PATH = '/root/named/za-tech.net.zone.tmp'
    # CONFIG_BAK_PATH = '/root/named/za-tech.net.zone.{}'.format(DATE)
    server = socketserver.TCPServer((HOST, PORT), TcpHandler)
    server.serve_forever()