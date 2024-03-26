#!/bin/bash
/home/dezs/projects/Scientific-research/spark/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.2 \
    --master spark://localhost:7077 \
    --driver-cores 2 \
    --driver-memory 3g \
    --num-executors 2 \
    --executor-memory 5g \
    --executor-cores 4 \
    --total-executor-cores 8 \
    /home/dezs/projects/Scientific-research/sparkApp.py
    # --conf spark.dynamicAllocation.enabled=true \
    # --conf spark.shuffle.service.enabled=true \
    # --conf spark.sh.speculation=true \
    # --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
    # --conf spark.sql.shuffle.partitions=12 \
    # --conf spark.default.parallelism=12 \
    # --conf spark.sql.autoBroadcastJoinThreshold=10485760 \
