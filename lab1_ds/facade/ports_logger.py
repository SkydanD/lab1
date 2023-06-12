from random import choice
from os import environ
from aiohttp import ClientSession, ClientError


class MixinRequest:
    
    @staticmethod
    async def get_massage_from_service(url: str, method: str, json: dict = None) -> dict:
        async with ClientSession(url) as session:
            async with session.request(url="/", method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()


class LoggerPorts(MixinRequest):
    proxys_servies = None
    
    @classmethod
    async def choose_service(cls) -> str:
        while True:
            choosen_serv = choice(cls.proxys_servies)
            try:
                await cls.get_massage_from_service(url=choosen_serv, method="GET")
                return choosen_serv
            except ClientError:
                print("Chosen service not work {}".format(choosen_serv)) 
                
    @staticmethod
    async def get_massage_from_service(url: str, method: str, json: dict = None) -> dict:
        async with ClientSession(url) as session:
            async with session.request(url="/", method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()
            

class Messgae(MixinRequest):
    proxys_servies = None
    
    @classmethod
    async def choose_service(cls) -> str:
        while True:
            choosen_serv = choice(cls.proxys_servies)
            try:
                await cls.get_massage_from_service(url=choosen_serv, method="GET")
                return choosen_serv
            except ClientError:
                print("Chosen service not work {}".format(choosen_serv)) 


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
        cls.message = []
        cls.loggin = []
        cls.nodes = []
        for number_service in range(1,3):
            cls.message.append(cls.info_service(f"api-message-{number_service}"))
            
        for number_service in range(1,4):
            cls.loggin.append(cls.info_service(f"api-loggin-{number_service}"))
            cls.nodes.append(cls.info_service(f"hazelcast-node-{number_service}"))
    