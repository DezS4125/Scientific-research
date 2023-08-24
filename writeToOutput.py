#ONLY FOR TESTING
from kafka import KafkaConsumer
import cv2
from CONSTANT import KAFKA_TOPIC_OUTPUT,BOOTSTRAP_SERVERS

consumer = KafkaConsumer(KAFKA_TOPIC_OUTPUT, bootstrap_servers=BOOTSTRAP_SERVERS)

for message in consumer:
    key = message.key
    value = message.value
    
    filename = f"/path/to/desired/directory/image-{key}.png"
    
    # Write the image data to the desired directory
    cv2.imwrite(filename, value)
