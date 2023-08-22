import cv2
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Set up the video capture
cap = cv2.VideoCapture("/home/ubuntu/codes/kafka/2023-08-17 11-47-34.mkv")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Encode the frame as a JPEG image
    ret, jpeg = cv2.imencode('.jpg', frame)

    # Send the encoded frame to the Kafka topic
    future = producer.send('video-stream-1', jpeg.tobytes())
    
    cv2.imshow('frame', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Handle any errors that may occur
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        pass

# Release the video capture when done
cap.release()