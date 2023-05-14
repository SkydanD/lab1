from aiohttp import web
from dotenv import load_dotenv
from os import environ
import json
from global_utils import HEADERS
load_dotenv()


app = web.Application()
local_hash_table = {}


async def get_massage(request):
    return web.Response(body=json.dumps(
            {
                'Response': list(local_hash_table.values())
                }
            ).encode('utf-8'), 
        headers=HEADERS
        )


async def create_message(request):
    data = await request.json()
    local_hash_table[data.get('uuid')] = data.get('message')
    print(local_hash_table)
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
        host=environ.get("HOST_LOGGIN"),
        port=environ.get("PORT_LOGGIN"),
        app=app
        )
