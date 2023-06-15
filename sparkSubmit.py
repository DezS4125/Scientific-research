import subprocess

subprocess.call(["/opt/spark/bin/spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0", "--master", "spark://192.168.1.252:7077", "/home/dezs/Projects/Scientific research/test/sparkApp.py"])




