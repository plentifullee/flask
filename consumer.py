from kafka import KafkaConsumer
import json

def main():
    topic = 'test-python-topic'
    # Create Kafka consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',  # Start reading from the beginning of the topic
        enable_auto_commit=True,
        group_id='my-group',  # Consumer group ID
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
    )

    print("Starting Kafka consumer...")
    print("Waiting for messages on topic: "+topic)

    try:
        # Continuously poll for new messages
        for message in consumer:
            print(f"Received message: {message.value}")
            print(f"Partition: {message.partition}")
            print(f"Offset: {message.offset}")
            print("------------------------")

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        # Close the consumer connection
        consumer.close()
        print("Consumer closed.")

if __name__ == "__main__":
    main()
