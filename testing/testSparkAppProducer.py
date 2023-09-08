from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from kafka import KafkaProducer
import random
from CONSTANT import BOOTSTRAP_SERVERS,KAFKA_TOPIC_RESULT


conf = SparkConf().setAppName("RandomKafkaProducer")
sc = SparkContext.getOrCreate(conf)
ssc = StreamingContext(sc, 1)

def send_to_kafka(rdd):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    for record in rdd.collect():
        producer.send(KAFKA_TOPIC_RESULT, str(record))
    producer.flush()

dstream = ssc.queueStream([sc.parallelize([random.randint(0, 1)]) for _ in range(100)])
dstream.foreachRDD(send_to_kafka)

ssc.start()
ssc.awaitTermination()
