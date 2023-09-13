#light weight version of webcamProduce.py

import cv2
import time
from kafka import KafkaProducer
import detectFaceYolov8 as det

# Set up a Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Set the topic to publish the video stream data to
topic = 'my-video-stream'

# Open a capture object for the webcam (0 for built-in webcam, 1 for external webcam)
cap = cv2.VideoCapture(0)

# Set up variables for calculating FPS
index=0
while True:
    index+=1
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # # Encode the frame as a JPG image
    # ret, buffer = cv2.imencode('.jpg', frame)

    # # Convert the image data to bytes and send to Kafka
    # producer.send(topic, buffer.tobytes())
    frame=det.processOneFaceInFrame(frame,index)
    # det.processOneFaceInFrame(frame,index)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # # Pause for 2 seconds
    # time.sleep(2)

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()