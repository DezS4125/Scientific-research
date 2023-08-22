from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from PIL import Image
import io
import cv2
import numpy as np
# import processing.janyDetection as jany

spark = SparkSession \
    .builder \
    .appName("Facial Analytic") \
    .getOrCreate()
    
# Subscribe to 1 topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.81.25:9092") \
    .option("subscribe", "video-stream-1") \
    .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

def process(batchDF, batchId):
    images = batchDF.select("value").rdd.map(lambda x: x["value"]).collect()
    for i, image in enumerate(images):
        filename = f"/home/ubuntu/codes/kafka/prod/output/image-{batchId}-{i}.png"
        # Convert the image data to a NumPy array
        nparr = np.frombuffer(image, np.uint8)
        
        # Decode the image data using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #image=cv2.imshow(image)
        # Display the frame in the window
        print("image received")
        cv2.imwrite(filename, image)

        # Check if the user pressed the 'q' key
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # result,img = jany.detectJany(image)
        # jany.workOnResults(result,image,filename) 

query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process) \
    .start()

query.awaitTermination()