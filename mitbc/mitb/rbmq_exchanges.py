import pika

from mitb import utils

utils = utils.utils()

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a headers exchange
exchange_name = 'header_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='headers')

# Create queues with header-based binding rules
queue_1 = 'header_queue_1'
queue_2 = 'header_queue_2'

# Declare the queues
channel.queue_declare(queue=queue_1)
channel.queue_declare(queue=queue_2)

# Set header rules for bindings
headers_1 = {'x-match': 'all', 'category': 'info', 'type': 'audit'}
headers_2 = {'x-match': 'any', 'category': 'error', 'type': 'log'}

# Bind queues with header rules to the exchange
channel.queue_bind(exchange=exchange_name, queue=queue_1, arguments=headers_1)
channel.queue_bind(exchange=exchange_name, queue=queue_2, arguments=headers_2)

# Publish messages with headers
message_1 = "Message with headers: info and audit"
message_2 = "Message with headers: error"

channel.basic_publish(
    exchange=exchange_name,
    routing_key='',
    body=message_1,
    properties=pika.BasicProperties(headers={'category': 'info', 'type': 'audit'})
)

channel.basic_publish(
    exchange=exchange_name,
    routing_key='',
    body=message_2,
    properties=pika.BasicProperties(headers={'category': 'error', 'type': 'log'})
)

print("Messages sent with headers.")

# JWT token generated for "rabbit_user"
jwt_token = utils.generate_jwt("rabbit_user")
print("JWT Token: %s" % (jwt_token))
# Configure the connection parameters
credentials = pika.PlainCredentials(username="rabbit_user", password=jwt_token)
parameters = pika.ConnectionParameters('localhost', 25672, '/', credentials)

# Declare a queue and send a message
channel.queue_declare(queue='test_queue')
channel.basic_publish(exchange='', routing_key='test_queue', body='Hello, JWT Auth!')

print("Message sent using JWT authentication")
connection.close()
