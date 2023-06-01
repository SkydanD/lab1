import time
import hazelcast
import threading

client = hazelcast.HazelcastClient( cluster_members=["192.168.1.101:5701","192.168.1.101:5702","192.168.1.101:5703"])
lock = client.get_map('my-distributed-map').blocking()

for i in range(1000):
 lock.set(i,i)
lock.set(1,0)
def thread_function2(name):
 for i in range(10000):
  val = lock.get(1)
 lock.set(1,val+1)
 print( f'Thread {name} done')
t = time.time()
threads = []
for index in range(10):
 x = threading.Thread(target=thread_function2, args=(index,))
 threads.append(x)
 x.start()
for thread in threads:
 thread.join()

print(time.time() - t)
print( lock.get(1))
