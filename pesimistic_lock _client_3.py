import time
import hazelcast
import threading


client_2 = hazelcast.HazelcastClient( cluster_members=["192.168.1.101:5701","192.168.1.101:5702","192.168.1.101:5703"])

lock_2 = client_2.get_map('my-distributed-map').blocking()
lock_2.set(1,0)


def thread_function2(name):
 for i in range(10000):
     lock_2.lock( 1 )
 try:
     val = lock_2.get(1)
     lock_2.set(1,val+1) 
 finally:
     lock_2.unlock( 1 )
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
print( lock_2.get(1))
