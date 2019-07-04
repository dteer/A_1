import pika
from config_client import severities
from item import *




def rabbitmq_client(severity='',message=''):
    #连接rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #声明队列
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')


    #声明主题
    # severity = sys.argv[1] if len(sys.argv) > 1 else 'info' #筛选级别
    # message = ' '.join(sys.argv[2:]) or 'Hello World!'

    #发送主题信息
    channel.basic_publish(exchange='direct_logs',
                          routing_key=severity,
                          body=message)
    #关闭rabbitmq
    connection.close()

def send():
    for severity in severities:
        message = eval(severity)()
        rabbitmq_client(severity,message)

if __name__ == '__main__':
    send()