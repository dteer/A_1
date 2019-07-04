#!/usr/bin/env python
import pika
from config_server import severities
from itme import *

# 接收到消息，做相应处理
def callback(ch, method, properties, body):
    eval(method.routing_key)(ch, method, properties, body)


def rec(severities):
    #连接rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    #声明队列
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')


    #本意是在命令行添加路由
    # severities = sys.argv[1:]
    # #如果为空，退出
    # if not severities:
    #     sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    #     sys.exit(1)

    #把队列绑定到交换机（路由）
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue


    #绑定不同路由到交换机
    for severity in severities:
        channel.queue_bind(exchange='direct_logs',
                           queue=queue_name,
                           routing_key=severity
                           )

    # 监听队列消息
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)
    #开始消费
    channel.start_consuming()

if __name__ == '__main__':
    rec(severities)