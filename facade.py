from aiohttp import web
from global_utils import request_to_server, HEADERS
from dotenv import load_dotenv
from os import environ
from uuid import uuid4
import json
load_dotenv()

app = web.Application()


async def get_massage(request): 
    
    response_from_message = await request_to_server(
        host=environ.get("HOST_MASSAGE"),
        port=environ.get("PORT_MASSAGE"),
        method="GET",
    )
    
    response_from_loggin = await request_to_server(
        host=environ.get("HOST_LOGGIN"),
        port=environ.get("PORT_LOGGIN"),
        method="GET"
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
        host=environ.get("HOST_LOGGIN"),
        port=environ.get("PORT_LOGGIN"),
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
        host=environ.get("HOST_FACADE"),
        port=environ.get("PORT_FACADE"),
        app=app
        )
