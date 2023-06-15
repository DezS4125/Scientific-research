import cv2
import time
from kafka import KafkaProducer


# Set up a Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Set the topic to publish the video stream data to
topic = 'webcam-video-stream'

# Open a capture object for the webcam (0 for built-in webcam, 1 for external webcam)
cap = cv2.VideoCapture(0)

# # Set up variables for calculating FPS
# fps = 0
# frame_count = 0
start_time = time.time()
last_sent_time = start_time

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # frame_count += 1    
    
    # Calculate elapsed time since last sent frame
    elapsed_time_since_sent = time.time() - last_sent_time
    
    # Check if at least 2 seconds have passed since last sent frame
    if elapsed_time_since_sent >= 2:
        # Encode the frame as a JPEG image
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert the image data to bytes and send to Kafka
        producer.send(topic, buffer.tobytes())
        
        # Print to screen
        print("Send image ....")
        
        # Update last sent time
        last_sent_time = time.time()
    
    # # Calculate FPS
    # elapsed_time = time.time() - start_time
    # if elapsed_time >= 1:
    #     fps = frame_count / elapsed_time
    #     frame_count = 0
    #     start_time = time.time()

    # # Display FPS on frame
    # cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()