from kafka import KafkaConsumer
from CONSTANT import BOOTSTRAP_SERVERS,KAFKA_TOPIC_RESULT

consumer = KafkaConsumer(KAFKA_TOPIC_RESULT, bootstrap_servers=BOOTSTRAP_SERVERS)

for message in consumer:
    print(message.value)