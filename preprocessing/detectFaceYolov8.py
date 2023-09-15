from ultralytics import YOLO
# import cv2
import os
# import sendImageToKafkaTopic as si

#Return a list of bounding box of faces
def detectFace(frame):
    # Load a model
    model = YOLO("/home/ubuntu/codes/kafka/prod/preprocessing/yolov8n-face.pt") # load a pretrained model (recommended for training)

    # Use the model
    results = model(frame) # predict on an image
    # Access the first result
    result = results[0]
    
    return result.boxes


##### !!! Should i check for every faces or just one face in each frame??#####

# # Process multiple faces in frame
# def processFacesInFrame(frame,frameIndex):
#     # Find every faces' coordinates in a frame
#     faces=detectFace(frame)
#     faceIndex=0
#     listOfImg=list()
#     for face in faces:
#         # Counting face
#         faceIndex+=1
#         # Get the box coordinates
#         x1, y1, x2, y2 = face.xyxy[0][:4]
        
#         # Convert coordinates to integers
#         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
#         cropped_img = frame[y1:y2, x1:x2]
        
#         listOfImg.append(cropped_img)
#     return listOfImg

# Process one face per frame
def processOneFaceInFrame(frame):
    # Find every faces' coordinates in a frame
    faces=detectFace(frame)
    if(faces):
        # Get the first face's coords
        face=faces[0]
        # Get the box coordinates
        x1, y1, x2, y2 = face.xyxy[0][:4]
        
        # Convert coordinates to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        cropped_img = frame[y1:y2, x1:x2]
        

        # # Send frame to kafka topic
        # si.sendImage(cropped_img)
        print("cropped image shape:")
        print(cropped_img.shape)
        return cropped_img