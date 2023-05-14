import hazelcast
client = hazelcast.HazelcastClient( cluster_members=["172.20.0.199:5701","172.20.0.199:5702","172.20.0.199:5703"])
client2 = hazelcast.HazelcastClient( cluster_members=["172.20.0.199:5701","172.20.0.199:5702","172.20.0.199:5703"])
client3 = hazelcast.HazelcastClient( cluster_members=["172.20.0.199:5701","172.20.0.199:5702","172.20.0.199:5703"])
q3 = client.get_queue('bqueue'). blocking()
q4 = client2.get_queue('bqueue'). blocking()
q5 = client3.get_queue('bqueue'). blocking()
for i in range(10):
 print(i)
 q3.offer( f"element {i}")
 print(print(q4.poll()))
 print(print(q5.poll()))
print(q3.iterator())

for i in range(10):
 q3.offer( f"element {i}")
print(q3.iterator())
q3.offer( f"element 20")
q3.offer( f"element 21")
print(q3.iterator())

