from kafka import KafkaConsumer
import cv2
import numpy as np

# Set up the Kafka consumer
consumer = KafkaConsumer('webcam-video-stream', bootstrap_servers=['localhost:9092'])

# Set up the window for displaying the video stream
cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)

for message in consumer:
    # Decode the JPEG image from the message value
    nparr = np.frombuffer(message.value, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the frame in the window
    cv2.imshow('Video Stream', frame)

    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the window when done
cv2.destroyAllWindows()
