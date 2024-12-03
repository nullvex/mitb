import pika
import threading
import time

class rbmq_consumer(threading.Thread):
    def __init__(self, host='localhost', queue='default_queue'):
        super().__init__()
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.stop_event = threading.Event()  # Event to stop the thread

    def connect(self):
        """Connect to RabbitMQ server and declare queue."""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        print(f"Connected to RabbitMQ on queue '{self.queue}'")

    def run(self):
        """Start the consumer thread."""
        self.connect()
        while not self.stop_event.is_set():
            method_frame, header_frame, body = self.channel.basic_get(self.queue, auto_ack=True)
            if method_frame:
                print(f"Received message: {body}")
                self.process_message(body)
            else:
                time.sleep(1)  # Wait before checking again if no message found

        # Clean up
        self.connection.close()
        print("Consumer thread stopped")

    def process_message(self, message):
        """Process incoming message (customizable based on application needs)."""
        print(f"Processing message: {message}")

    def stop(self):
        """Stop the consumer thread."""
        self.stop_event.set()

