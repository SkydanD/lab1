from aiohttp import web
from os import environ
import json
from global_utils import HEADERS
from base_client import MapHz


app = web.Application()
instance_map = MapHz(
    list_nodes=[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
    cluster_name="dev"
)
instance_map.create_map("map_custom")


async def get_massage(request):
    return web.Response(body=json.dumps(
            {
                'Response': instance_map.map_dist.values().result() if instance_map.map_dist.size().result() else "Not Found Data"
                }
            ).encode('utf-8'), 
        headers=HEADERS
        )


async def create_message(request):
    data = await request.json()
    instance_map.send_data(unique_id=data.get('uuid'), massange=data.get('message'))
    print(f"{data.get('uuid')} = {data.get('message')}")
    return web.Response(body=json.dumps(
            {
                'Response': data
                }
            ).encode('utf-8'), 
        headers=HEADERS
        )
    



app.add_routes([
    web.get('/', get_massage),
    web.post('/', create_message)
])


if __name__ == "__main__":
    web.run_app(
        host="0.0.0.0",
        port=environ.get("PORT_SEVICE"),
        app=app
        )
