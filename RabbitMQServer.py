# -*- coding:UTF-8 -*-
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.56.101')
    )

channel = connection.channel()
channel.queue_declare(queue='hello', durable=True)   # durable 持久化队列(只持久化对列名称)

channel.basic_publish(exchange='', 
    routing_key='hello',
    body='Hello world!',
    properties=pika.BasicProperties(delivery_mode=2)   # 持久化队列内容 
    )
print ('[x] sent hello world')

connection.close()