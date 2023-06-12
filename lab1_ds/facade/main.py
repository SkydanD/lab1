from aiohttp import web
from global_utils import request_to_server, HEADERS
from ports_logger import LoggerPorts, Messgae, GetInfoService
from os import environ
from uuid import uuid4
import json
from base_client import QuieneHz
from asyncio import get_event_loop

loop = get_event_loop()
loop.run_until_complete(GetInfoService.get_all_services())

instance_qu = QuieneHz(
    list_nodes=GetInfoService.nodes, 
    cluster_name="dev"
)
instance_qu.create_quein("qu_custom")
LoggerPorts.proxys_servies = GetInfoService.loggin
Messgae.proxys_servies = GetInfoService.message


app = web.Application()


async def get_massage(request): 
    response_from_message = ' meessage = '

    response_from_message += await request_to_server(
        domain=await Messgae().choose_service()
    )
    
    response_from_loggin = await request_to_server(
        domain=await LoggerPorts().choose_service()
    )
    response_from_message += "\n logger"
    
    for message_from_log in response_from_loggin:
        response_from_message += message_from_log
        
    return web.Response(
        body=json.dumps(
            {
                'Response': response_from_message
                }
            ).encode('utf-8'), 
        headers=HEADERS
        )


async def save_massage(request):
    data = await request.json()
    await request_to_server(
        domain=await LoggerPorts().choose_service(),
        method="POST",
        json={
            "uuid": str(uuid4()),
            "message": data.get("message")
            }
    )
    
    await instance_qu.send_data(data.get("message"))
    
    return web.Response(
        body=json.dumps(
            {
                'Response': data
                }
            ).encode('utf-8'), 
        headers=HEADERS
        )


app.add_routes([
    web.get('/', get_massage),
    web.post('/', save_massage)
])


if __name__ == "__main__":
    web.run_app(
        host="0.0.0.0",
        port=environ.get("PORT_SEVICE"),
        app=app
        )
