import subprocess

subprocess.call(["/opt/spark/bin/spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0", "--master", "spark://192.168.81.106:7077", "/home/ubuntu/codes/kafka/prod/sparkApp.py"])




