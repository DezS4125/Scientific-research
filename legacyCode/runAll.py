import subprocess
import time

# Start Zookeeper, Kafka server and Spark Cluster script
subprocess.Popen(['/home/dezs/anaconda3/envs/SciRe/bin/python', '/home/dezs/Projects/Scientific research/prod/startServers.py'])
# time.sleep(10)
# Start producer
subprocess.Popen(['/home/dezs/anaconda3/envs/SciRe/bin/python', '/home/dezs/Projects/Scientific research/test/webcamProducer.py'])
time.sleep(5)
# Start Spark app
subprocess.Popen(['/home/dezs/anaconda3/envs/SciRe/bin/python', '/home/dezs/Projects/Scientific research/test/sparkSubmit.py'])