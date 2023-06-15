import processing.janyDetection as jany
import cv2

imgPath = '/home/dezs/Pictures/Screenshot_20230614_143049.png'
image=cv2.imread(imgPath)
result,img = jany.detectJany(image)
jany.workOnResults(result,image) 