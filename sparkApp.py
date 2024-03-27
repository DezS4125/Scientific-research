from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import cv2
from kafka import KafkaProducer
import numpy as np
import time
from CONSTANT import APP_NAME,KAFKA_TOPIC_INPUT,BOOTSTRAP_SERVERS,KAFKA_TOPIC_OUTPUT,BOOTSTRAP_SERVERS_FOR_SPARK
# from TRained_model.DENSE.src.prediction import predict_image
# from tensorflow.keras.models import load_model
import model.vit_cam_dect as vit
# import model.cnn_cam_dect as cnn
import model.camera as ca


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


producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)



def process(batchDF, batchId):
    images = batchDF.select("value").rdd.map(lambda x: x["value"]).collect()
    for i, image in enumerate(images):
        # Convert the image data to a NumPy array
        nparr = np.frombuffer(image, np.uint8)

        # Decode the image data using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Drowsiness prediction using VIT
        prediction, resultFrame=ca.predict(image,vit.model)
        # # Drowsiness prediction using CNN
        # prediction, resultFrame=ca.predict(image,cnn.model)
        print(prediction)

        message = str(prediction).encode('utf-8')
        producer.send(KAFKA_TOPIC_OUTPUT, message)


        # cv2.imshow('frame', image)

        # # Exit the loop when 'q' key is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        


query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process) \
    .start()

query.awaitTermination()