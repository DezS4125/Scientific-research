#ONLY FOR TESTING
from kafka import KafkaConsumer
import cv2
import numpy as np
from CONSTANT import KAFKA_TOPIC_OUTPUT,BOOTSTRAP_SERVERS

consumer = KafkaConsumer(KAFKA_TOPIC_OUTPUT, bootstrap_servers=BOOTSTRAP_SERVERS)
print ("Consumer is up")
index = 0
for message in consumer:
    value = message.value
    cv2.imwrite("/home/ubuntu/codes/kafka/output/image-" + str(index) + ".jpg", frame)
    # print(message.value)
    print("Received image")
    