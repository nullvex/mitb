import pika

class rbmq_producer:
    def __init__(self, host='localhost', queue='default_queue'):
        self.host = host
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def publish(self, message):
        """Publish a message to the queue."""
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        print(f"Sent message: {message}")

    def close(self):
        """Close the connection."""
        self.connection.close()

