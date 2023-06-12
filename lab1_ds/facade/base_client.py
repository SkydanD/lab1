from hazelcast import HazelcastClient
from dataclasses import dataclass, field
from asyncio import sleep


@dataclass
class ClientOperator():
    list_nodes: list
    cluster_name: str
    
    def __post_init__(self):
        self._client = HazelcastClient(
            cluster_name=self.cluster_name, 
            cluster_members=self.list_nodes
            )
    

class MapHz(ClientOperator):
    
    def create_map(self, name_map: str):
        self.map_dist = self._client.get_map(name_map)

    
    def send_data(self, unique_id: str, massange: str) -> str:
        self.map_dist.set(unique_id, massange).result()
        return self.map_dist.get(unique_id).result()
    

class QuieneHz(ClientOperator):
    
    def create_quein(self, name_qu: str):
        self.quiene_hz = self._client.get_queue(name_qu)
        
    async def send_data(self, message: str):
        self.quiene_hz.put(message).result()
    
    async def get_and_check_element(self):
        if (element := self.quiene_hz.poll().result()) is None:
            return await sleep(1)
        await sleep(1)
        return element
