from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import cv2
import numpy as np
from io import BytesIO
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

print("hello 1")
def process(row):
    image = row["value"]
    filename = f"/home/ubuntu/codes/kafka/prod/output/image-{row['key']}.png"
    print("hello 2")

    # Convert the image data to a NumPy array
    nparr = np.frombuffer(image, np.uint8)
    
    # Decode the image data using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Display the frame in the window
    print("image received")
    
    # Serialize the image data
    img_bytes = BytesIO()
    np.save(img_bytes, image)
    
    # Publish the image data to a Kafka topic
    try:
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        producer.send(KAFKA_TOPIC_OUTPUT, key=row['key'], value=img_bytes.getvalue())
        producer.flush()
        print("image sent to kafka topic")
    except Exception as e:
        print(f"Error sending message to Kafka: {e}")
    finally:
        producer.close()

# Start the streaming query
query = df \
    .writeStream \
    .outputMode("append") \
    .foreach(process) \
    .start()

query.awaitTermination()
