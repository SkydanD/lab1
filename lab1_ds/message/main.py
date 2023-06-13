from aiohttp import web
from os import environ
import json
from global_utils import HEADERS
from base_client import QuieneHz, GetInfoService
from asyncio import new_event_loop

loop = new_event_loop()
loop.run_until_complete(GetInfoService.get_all_services())

app = web.Application()

instance_qu = QuieneHz(
    list_nodes=GetInfoService.nodes, 
    cluster_name="dev"
)

instance_qu.create_quein("qu_custom")
list_all = []

async def background_process():
    while True:
        print("wait")
        element = await instance_qu.get_and_check_element()
        if element is not None:
            print("heh")
            list_all.append(element) 
        

async def startup_background_process(app):
    app['background_process'] = app.loop.create_task(background_process())

async def cleanup_background_process(app):
    app['background_process'].cancel()
    await app['background_process']


async def get_massage(request):
    str_tmp = ""
    for str_in_list in list_all:
        str_tmp += f"{str_in_list}\n"
    return web.Response(body=json.dumps(
            {
                'Response': str_tmp
                }
            ).encode('utf-8'), 
        headers=HEADERS)


app.add_routes([
    web.get('/', get_massage)
])

app.on_startup.append(startup_background_process)
app.on_cleanup.append(cleanup_background_process)


if __name__ == "__main__":
    web.run_app(
        host="0.0.0.0",
        port=environ.get("PORT_SEVICE"),
        app=app
        )
