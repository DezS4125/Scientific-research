from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import cv2
import numpy as np
from CONSTANT import APP_NAME,KAFKA_TOPIC_INPUT,BOOTSTRAP_SERVERS,KAFKA_TOPIC_OUTPUT,BOOTSTRAP_SERVERS_FOR_SPARK
from TRained_model.DENSE.src.prediction import predict_image
from tensorflow.keras.models import load_model


spark = SparkSession \
    .builder \
    .appName(APP_NAME) \
    .getOrCreate()
    
# Subscribe to 1 topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS_FOR_SPARK) \
    .option("subscribe", KAFKA_TOPIC_INPUT) \
    .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


# Load the trained model
model_path = "/home/ubuntu/codes/kafka/prod/TRained_model/DENSE/model/output_model/cluster/model2_224x224/cluster_densenet_224x224.h5"
model = load_model(model_path)

def process(batchDF, batchId):
    images = batchDF.select("value").rdd.map(lambda x: x["value"]).collect()
    for i, image in enumerate(images):
        # Convert the image data to a NumPy array
        nparr = np.frombuffer(image, np.uint8)
        
        # Decode the image data using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process the image as needed
        index,prob=predict_image(model, image)
        print("index="+index+"; prob="+prob)
        # Encode the processed image as a JPEG
        # ret, buf = cv2.imencode(".jpg", image)
        # image_bytes = buf.tobytes()
        
        # # Create a DataFrame with the processed image data
        # image_df = spark.createDataFrame([(image_bytes,)], ["value"])
        
        # # Write the processed image to a Kafka topic
        # image_df \
        #     .selectExpr("CAST(value AS STRING)") \
        #     .write \
        #     .format("kafka") \
        #     .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS_FOR_SPARK) \
        #     .option("topic", KAFKA_TOPIC_OUTPUT) \
        #     .save()


query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process) \
    .start()

query.awaitTermination()