from kafka import KafkaConsumer
from CONSTANT import KAFKA_TOPIC_OUTPUT,BOOTSTRAP_SERVERS,DROWSY_CONFIRM_PERCENTAGE
consumer = KafkaConsumer(KAFKA_TOPIC_OUTPUT, bootstrap_servers=BOOTSTRAP_SERVERS)

window = []
for message in consumer:
    value = int(message.value.decode())
    window.append(value)
    if len(window) > 12:
        window.pop(0)
        print(window)
        print(sum(window))
    if sum(window) > 12*DROWSY_CONFIRM_PERCENTAGE:
        print("DROWSYYYYY!!!!!!!!!")