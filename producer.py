from kafka import KafkaProducer
import json
import time
from datetime import datetime

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def main():
    # Create Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=['192.168.10.105:9092'],
        value_serializer=json_serializer
    )

    topic = 'test-python-topic'

    print("Starting Kafka producer...")
    print("Sending messages to topic: "+topic)

    try:
        message_count = 1
        while True:
            # Create a sample message with timestamp
            message = {
                "id": message_count,
                "message": f"Test message {message_count}",
                "timestamp": datetime.now().isoformat()
            }

            # Send the message
            future = producer.send(topic, value=message)
            # Wait for message to be delivered
            record_metadata = future.get(timeout=10)
            
            print(f"Message sent: {message}")
            print(f"Partition: {record_metadata.partition}")
            print(f"Offset: {record_metadata.offset}")
            print("------------------------")

            message_count += 1
            time.sleep(2)  # Wait 2 seconds between messages

    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        # Flush and close the producer
        producer.flush()
        producer.close()
        print("Producer closed.")

if __name__ == "__main__":
    main()
