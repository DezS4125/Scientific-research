from kafka import KafkaConsumer
from CONSTANT import KAFKA_TOPIC_OUTPUT,BOOTSTRAP_SERVERS,DROWSY_CONFIRM_PERCENTAGE
consumer = KafkaConsumer(KAFKA_TOPIC_OUTPUT, bootstrap_servers=BOOTSTRAP_SERVERS)

window = []
for message in consumer:
    value = int(message.value.decode())
    window.append(value)
    print(window)
    print(str(window.count(0)) + "," + str(0.7 * len(window)))
    if len(window) > 12:
        window.pop(0)
        if window.count(0) > 0.7 * len(window):
            print("DROWSYYYY!!!!!!!!!")