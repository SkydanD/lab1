import time
import hazelcast
import threading

client = hazelcast.HazelcastClient( cluster_members=["192.168.1.101:5701","192.168.1.101:5702","192.168.1.101:5703"])
lock = client.get_map('my-distributed-map').blocking()
lock.set(1,0)
def thread_function2(name):
 for i in range(10000):
     lock.lock( 1 )
 try:
     val = lock.get(1)
     lock.set(1,val+1) 
 finally:
     lock.unlock( 1 )
     print( f'Thread {name} done')
threads = []
t =time.time()
for index in range(10):
     x = threading.Thread(target=thread_function2, args=(index,))
     threads.append(x)
     x.start()
for thread in threads:
 thread.join()



print( time.time()-t)
print( lock.get(1))
