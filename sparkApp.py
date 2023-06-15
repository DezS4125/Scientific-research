from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from PIL import Image
import io
import cv2
import numpy as np
import processing.janyDetection as jany

spark = SparkSession \
    .builder \
    .appName("Facial Analytic") \
    .getOrCreate()
    
# Subscribe to 1 topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.1.252:9092") \
    .option("subscribe", "webcam-video-stream") \
    .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

def process(batchDF, batchId):
    images = batchDF.select("value").rdd.map(lambda x: x["value"]).collect()
    for i, image in enumerate(images):
        filename = f"output/image-{batchId}-{i}.png"
        # Convert the image data to a NumPy array
        nparr = np.frombuffer(image, np.uint8)
        
        # Decode the image data using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # image=cv2.imread(image)
        result,img = jany.detectJany(image)
        jany.workOnResults(result,image,filename) 

query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process) \
    .start()

query.awaitTermination()