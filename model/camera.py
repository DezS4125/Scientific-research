import cv2
import numpy as np
import time


RED = (0, 0, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)


def preprocess(image):
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cv2.imshow("Face", image)
    # image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image

def predict(face,model):
    face = preprocess(face)
    print(face.shape)
    result = model.predict(face)
    index = np.argmax(result)
    label = ["DROWSY", "NON DROWSY"]	
    label = label[index]
    # if index == 0:
    #     cv2.putText(face, label, (0,0), cv2.FONT_HERSHEY_SIMPLEX, 2, RED, 2)
    # else:
    #     cv2.putText(face, label, (0,0), cv2.FONT_HERSHEY_SIMPLEX, 2, GREEN, 2)
    print(label)
    return index, face

# def get_camera_detect(model_face, model):
#     camera = cv2.VideoCapture(0)
#     while True:
#         _, frame = camera.read()
#         prev_time = time.time()
#         result = model_face(frame, show=False)
#         # print(result[0].boxes.xyxy.tolist()[0][1])
#         boxes = result[0].boxes
#         for box in boxes:
#             top_left_x = int(box.xyxy.tolist()[0][0])
#             top_left_y = int(box.xyxy.tolist()[0][1])
#             bot_right_x = int(box.xyxy.tolist()[0][2])
#             bot_right_y = int(box.xyxy.tolist()[0][3])
#             cv2.rectangle(frame, (top_left_x, top_left_y), (bot_right_x, bot_right_y), (0, 0, 255), 2)    
#             print(top_left_x, top_left_y, bot_right_x, bot_right_y)
#             print("****************")
#             face = frame[top_left_y:bot_right_y, top_left_x:bot_right_x]
            
            
#             if face.shape[0] > 0 and face.shape[1] > 0:
#                 face = preprocess(face)
#                 print(face.shape)

#                 result = model.predict(face)
#                 index = np.argmax(result)
#                 label = ["DROWSY", "NON DROWSY"]	
#                 label = label[index]
#                 if index == 0:
#                     cv2.putText(frame, label, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 2, RED, 2)
#                 else:
#                     cv2.putText(frame, label, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 2, GREEN, 2)
#                 print(label)
#         # Calculate FPS
#         current_time = time.time()
#         fps = 1.0 / (current_time - prev_time)
#         prev_time = current_time

#         # Display FPS on the frame
#         cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, BLUE, 2)
            
            
#         # cv2.putText(frame, str(count), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 1)    
#         cv2.imshow("Frame", frame)
#         if cv2.waitKey(10) & 0xFF==27:
#             break    