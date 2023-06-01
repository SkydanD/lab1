import hazelcast
if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient()
    hz2 = hazelcast.HazelcastClient()
    hz3 = hazelcast.HazelcastClient()
    # Get the Distributed Map from Cluster.
    map = hz.get_map("my-distributed-map").blocking()
    # Standard Put and Get
    for i in range(0, 1001):
        map.put(i, i)
        map.get(i)
        print(i)
        
    # Concurrent Map methods, optimistic updating
    map.put_if_absent("somekey", "somevalue")
    map.replace_if_same("key", "value", "newvalue")
    # Shutdown this Hazelcast Client
    hz.shutdown()