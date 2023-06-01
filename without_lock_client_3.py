import time
import hazelcast
import threading

client_2 = hazelcast.HazelcastClient( cluster_members=["192.168.1.101:5701","192.168.1.101:5702","192.168.1.101:5703"])
lock_2 = client_2.get_map('my-distributed-map').blocking()

for k in range(1000):
 lock_2.set(k,k)
lock_2.set(1,0)
def thread_function2(name):
 for i in range(10000):
  val = lock_2.get(1)
 lock_2.set(1,val+1)
 print( f'Thread {name} done')
t_2 = time.time()
threads = []
for index in range(10):
 x_2 = threading.Thread(target=thread_function2, args=(index,))
 threads.append(x_2)
 x_2.start()
for thread in threads:
 thread.join()

print(time.time() - t_2)
print( lock_2.get(1))