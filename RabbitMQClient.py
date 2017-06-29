#-*- coding:UTF-8 -*-
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.56.101')
    )

channel = connection.channel()
channel.queue_declare('hello', durable=True)

def callback(ch, method, properties, body):
    print ("ch --> {}, method --> {}, properties --> {}".format(ch, method, properties))
    print ('[x] Received {}'.format(body))
    channel.basic_ack(delivery_tag=method.delivery_tag) # 想向服务器发送确认消息

channel.basic_consume(callback, 
    queue='hello',
    no_ack=True)

print ("[*] Waiting from message. To exit press Ctrl+C")
channel.start_consuming()