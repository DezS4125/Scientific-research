from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import cv2
import numpy as np
from CONSTANT import APP_NAME,KAFKA_TOPIC,BOOTSTRAP_SERVERS

spark = SparkSession \
    .builder \
    .appName(APP_NAME) \
    .getOrCreate()
    
# Subscribe to 1 topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

def process(row):
    image = row["value"]
    filename = f"/home/ubuntu/codes/kafka/prod/output/image-{row['key']}.png"
    
    # Convert the image data to a NumPy array
    nparr = np.frombuffer(image, np.uint8)
    
    # Decode the image data using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Display the frame in the window
    print("image received")
    cv2.imwrite(filename, image)

query = df \
    .writeStream \
    .outputMode("append") \
    .foreach(process) \
    .start()

query.awaitTermination()
