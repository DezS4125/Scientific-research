import cv2

# Options to video captures
def captureWebcam():
    # Open a capture object for the webcam (0 for built-in webcam, 1 for external webcam)
    cap = cv2.VideoCapture(0)
    return cap

def captureVideo(videoPath):
    # Open a capture object for the webcam (0 for built-in webcam, 1 for external webcam)
    cap = cv2.VideoCapture(videoPath)
    return cap