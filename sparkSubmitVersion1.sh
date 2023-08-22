#!/bin/bash
/opt/spark/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
    --master spark://192.168.81.106:7077 \
    --executor-memory 6g \
    --driver-memory 6g \
    --num-executors 3 \
    --executor-cores 4 \
    --conf spark.dynamicAllocation.enabled=true \
    --conf spark.shuffle.service.enabled=true \
    --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
    --conf spark.sql.shuffle.partitions=8 \
    --conf spark.sql.autoBroadcastJoinThreshold=10485760 \
    /home/ubuntu/codes/kafka/prod/sparkApp.pya
