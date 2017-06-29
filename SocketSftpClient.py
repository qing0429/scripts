#-*- coding:UTF-8 -*-
import socket, sys, hashlib


client = socket.socket()
client.connect(('10.139.96.117', 1024))

while True:
    cmd = raw_input('# ').strip()
    if len(cmd) == 0: continue
    if cmd.startswith('get'):
        op, filename = cmd.split()
        client.send(filename)
        server_reps = client.recv(1024)
        print "file total size: {}".format(server_reps)
        #client.send('start recv data')
        file_total_size = int(server_reps)
        recv_size = 0
        f = open(filename.split('/')[-1] + '.new', 'wb')
        m = hashlib.md5()
        while recv_size < file_total_size:
            # 根据接受到的文件大小来设置接受数据的缓存
            if file_total_size - recv_size > 1024:
                size = 1024
            else:
                size = file_total_size - recv_size

            print "--{}--{}--{}--".format(file_total_size, recv_size, size)

            data = client.recv(size)
            m.update(data)
            recv_size += len(data)
            f.write(data)
        else:
            f.close()
            
        src_file_md5 = client.recv(1024)
        local_file_md5 = m.hexdigest()
        if src_file_md5 == local_file_md5:
            print "well done"
            print "{} <> {}".format(src_file_md5, local_file_md5)

