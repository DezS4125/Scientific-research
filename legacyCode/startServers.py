import os
import subprocess
import time

os.chdir(os.path.expanduser("~/kafka"))
subprocess.Popen(["bin/zookeeper-server-start.sh", "config/zookeeper.properties"])
time.sleep(5)
subprocess.Popen(["bin/kafka-server-start.sh", "config/server.properties"])
subprocess.Popen(["/opt/spark/sbin/start-all.sh"])