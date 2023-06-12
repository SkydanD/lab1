from hazelcast import HazelcastClient
from dataclasses import dataclass, field
from asyncio import sleep
from aiohttp import ClientSession


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


class GetInfoService:
    
    @classmethod
    async def get_service_name(cls, method: str = "GET", url: str = "/", json: dict = None) -> dict:
        async with ClientSession("http://consul-service:8500") as session:
            async with session.request(url=url, method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()
    
    @classmethod
    async def info_service(cls, name_service) -> str:
        info_service = await cls.get_service_name(
                        url="/v1/catalog/service/{service_name}".format(
                            service_name= name_service
                    ))
        info_service = info_service[0]
        return "http://{addres}:{ports}".format(
            addres=info_service["ServiceName"],
            ports=info_service["ServicePort"]
            )
     
    @classmethod
    async def get_all_services(cls):
        cls.nodes = []
            
        for number_service in range(1,4):
            cls.nodes.append(cls.info_service(f"hazelcast-node-{number_service}"))
