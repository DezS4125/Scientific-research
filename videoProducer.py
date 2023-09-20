import cv2
from kafka import KafkaProducer
from kafka.errors import KafkaError
from CONSTANT import KAFKA_TOPIC_INPUT,BOOTSTRAP_SERVERS
import preprocessing.detectFaceYolov8 as det

# logging.basicConfig(level=logging.DEBUG)

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

# Set up the video capture
cap = cv2.VideoCapture("/home/ubuntu/codes/kafka/2023-08-17 11-47-34.mkv")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    print("####################")
    # frame=det.processOneFaceInFrame(frame)

    # Encode the frame as a JPEG image
    ret, jpeg = cv2.imencode('.jpg', frame)
    # Send the encoded frame to the Kafka topic
    future = producer.send(KAFKA_TOPIC_INPUT, jpeg.tobytes())
    print("Message sent!")
    
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as e:
        # Decide what to do if produce request failed...
        print ("Message sent failed")
        print (f"Error: {e}")
        pass
    # cap.release()

# Release the video capture when done
cap.release()