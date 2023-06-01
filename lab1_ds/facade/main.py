from aiohttp import web
from global_utils import request_to_server, HEADERS
from ports_logger import LoggerPorts
from os import environ
from uuid import uuid4
import json


app = web.Application()


async def get_massage(request): 
    
    response_from_message = await request_to_server(
        domain="http://{host}:{port}".format(
            host="api-message",
            port=environ.get("PORT_MESSAGE")
            )
    )
    
    response_from_loggin = await request_to_server(
        domain=await LoggerPorts().choose_service()
    )
    
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
