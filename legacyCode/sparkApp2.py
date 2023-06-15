from pyspark.sql import SparkSession
from pyspark.sql.functions import *
# from PIL import Image
# import io
import cv2
import numpy as np

spark = SparkSession \
    .builder \
    .appName("Facial Analytic") \
    .getOrCreate()
    
# Subscribe to 1 topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "webcam-video-stream") \
    .load()
# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

def process(batchDF, batchId):
    images = batchDF.select("value").rdd.map(lambda x: x["value"]).collect()
    # images = batchDF.select("value").collect()
    for i, image in enumerate(images):
        # Convert bytearray to numpy array
        image_np = np.frombuffer(image, dtype=np.uint8)
        
        # Decode the image
        image_decoded = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        # Define the output filename
        filename = f"output/image-{batchId}-{i}.jpg"
        
        # Save the image to disk
        cv2.imwrite(filename, image_decoded)

query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process) \
    .start()

query.awaitTermination()