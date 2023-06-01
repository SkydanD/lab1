import time
import hazelcast
import threading

client_1 = hazelcast.HazelcastClient( cluster_members=["192.168.1.101:5701","192.168.1.101:5702","192.168.1.101:5703"])
lock_1 = client_1.get_map('my-distributed-map').blocking()


for j in range(1000):
 lock_1.set(j,j)
lock_1.set(1,0)
def thread_function2(name):
 for i in range(10000):
  val = lock_1.get(1)
 lock_1.set(1,val+1)
 print( f'Thread {name} done')
t_1 = time.time()
threads = []
for index in range(10):
 x_1 = threading.Thread(target=thread_function2, args=(index,))
 threads.append(x_1)
 x_1.start()
for thread in threads:
 thread.join()

print(time.time() - t_1)
print( lock_1.get(1))