import json
def chrome(ch, method, properties, body):
    body = json.loads(body.decode('utf8'))
    print(" [x] %r:%r" % (method.routing_key, body))

def test(ch, method, properties, body):
    body = json.loads(body.decode('utf8'))
    print(" [x] %r:%r" % (method.routing_key, body))