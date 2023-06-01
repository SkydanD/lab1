from aiohttp import web
from os import environ
import json
from global_utils import HEADERS
from base_client import QuieneHz
from asyncio import create_task

app = web.Application()
instance_qu = QuieneHz(
    list_nodes=[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
    cluster_name="dev"
)

instance_qu.create_quein("qu_custom")
list_all = []


async def check_massage():
    while True:
        element = await instance_qu.get_and_check_element()
        if element is not None:
           list_all.append(element) 


async def start_background_task(app):
    app['background_task'] = create_task(check_massage())



async def get_massage(request):
    return web.Response(body=json.dumps(
            {
                'Response': list_all
                }
            ).encode('utf-8'), 
        headers=HEADERS)


app.add_routes([
    web.get('/', get_massage)
])

app.on_startup.append(start_background_task)


if __name__ == "__main__":
    web.run_app(
        host="0.0.0.0",
        port=environ.get("PORT_SEVICE"),
        app=app
        )
