from ultralytics import YOLO
import cv2
import os
import sendImageToKafkaTopic as si

#Return a list of bounding box of faces
def detectFace(frame):
    # Create the output directory if it doesn't exist
    output_dir = '/home/dezs/Projects/Scientific research/ML stuff/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Load a model
    model = YOLO("yolov8n-face.pt") # load a pretrained model (recommended for training)

    # Use the model
    results = model(frame) # predict on an image
    # Access the first result
    result = results[0]
    
    return result.boxes


##### !!! Should i check for every faces or just one face in each frame??#####

# Process multiple faces in frame
def processFacesInFrame(frame,frameIndex):
    # Find every faces' coordinates in a frame
    faces=detectFace(frame)
    faceIndex=0
    listOfImg=list()
    for face in faces:
        # Counting face
        faceIndex+=1
        # Get the box coordinates
        x1, y1, x2, y2 = face.xyxy[0][:4]
        
        # Convert coordinates to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        # # Draw a rectangle on the image
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Crop the image using the box coordinates
        cropped_img = frame[y1:y2, x1:x2]
        
        # # Create the output directory if it doesn't exist
        # output_dir = '/home/dezs/Projects/Scientific research/ML stuff/output'
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        # # Save the cropped image to a file
        # filename = f'{output_dir}/image_{frameIndex}_{faceIndex}.jpg'
        # cv2.imwrite(filename, cropped_img)
        listOfImg.append(cropped_img)
    return listOfImg

# Process one face per frame
def processOneFaceInFrame(frame,frameIndex):
    # Find every faces' coordinates in a frame
    faces=detectFace(frame)
    if(faces):
        # Get the first face's coords
        face=faces[0]
        # Get the box coordinates
        x1, y1, x2, y2 = face.xyxy[0][:4]
        
        # Convert coordinates to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        # # Draw a rectangle on the image
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Crop the image using the box coordinates
        cropped_img = frame[y1:y2, x1:x2]
        
        # Send frame to kafka topic
        si.sendImage(cropped_img)
        
        # ###Below are just for testing purposes, remove before push it into prod
        # # Create the output directory if it doesn't exist
        # output_dir = '/home/dezs/Projects/Scientific research/ML stuff/output'
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        # # Save the cropped image to a file
        # filename = f'{output_dir}/image_{frameIndex}.jpg'
        # cv2.imwrite(filename, cropped_img)
        # ###end test
        return cropped_img