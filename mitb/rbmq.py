import pika
import threading
import time

class RabbitMQConnectionManager:
    def __init__(self, host='localhost', queue='default_queue'):
        self.host = host
        self.queue = queue
        self


