#!/bin/bash
/opt/spark/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
    --master spark://192.168.81.106:7077 \
    --driver-cores 4 \
    --driver-memory 3g \
    --num-executors 3 \
    --executor-memory 5g \
    --executor-cores 4 \
    --total-executor-cores 12 \
    /home/ubuntu/codes/kafka/prod/sparkApp.py
    # --conf spark.dynamicAllocation.enabled=true \
    # --conf spark.shuffle.service.enabled=true \
    # --conf spark.sh.speculation=true \
    # --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
    # --conf spark.sql.shuffle.partitions=12 \
    # --conf spark.default.parallelism=12 \
    # --conf spark.sql.autoBroadcastJoinThreshold=10485760 \
