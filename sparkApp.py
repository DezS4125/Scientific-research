from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import cv2
import numpy as np
from kafka import KafkaProducer
from CONSTANT import APP_NAME,KAFKA_TOPIC_INPUT,BOOTSTRAP_SERVERS,KAFKA_TOPIC_OUTPUT

spark = SparkSession \
    .builder \
    .appName(APP_NAME) \
    .getOrCreate()
    
# Subscribe to 1 topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC_INPUT) \
    .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

def process(batchDF, batchId):
    images = batchDF.select("value").rdd.map(lambda x: x["value"]).collect()
    for i, image in enumerate(images):
        # Convert the image data to a NumPy array
        nparr = np.frombuffer(image, np.uint8)
        
        # Decode the image data using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process the image as needed
        # ...
        
        # Encode the processed image as a JPEG
        ret, buf = cv2.imencode(".jpg", image)
        image_bytes = buf.tobytes()
        
        # Write the processed image to a Kafka topic
        producer.send(KAFKA_TOPIC_OUTPUT, value=image_bytes)

query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process) \
    .start()

query.awaitTermination()