import rbmq_producer
import rbmq_consumer

if __name__ == "__main__":
    # Initialize producer and consumer
    producer = rbmq_producer.rbmq_producer(queue='test_queue')
    consumer = rbmq_consumer.rbmq_consumer(queue='test_queue')

    consumer.start()

    # Send some test messages
    for i in range(5):
        producer.publish(f"Test message {i}")
        time.sleep(0.5)

    # Allow some time for messages to be processed
    time.sleep(5)

    # Stop the consumer and close producer connection
    consumer.stop()
    consumer.join()  # Wait for the consumer thread to finish
    producer.close()

