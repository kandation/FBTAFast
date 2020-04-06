import time, os

start_time = time.time()
if os.path.exists('./emergency_cluster_stop.stop'):
    print('has File')
os.remove('./emergency_cluster_stop.stop')
print(time.time()- start_time)