from aiohttp import web
from os import environ
import json
from global_utils import HEADERS

app = web.Application()


async def get_massage(request):
    return web.Response(body=json.dumps(
            {
                'Response': 'Not implemented'
                }
            ).encode('utf-8'), 
        headers=HEADERS)


app.add_routes([
    web.get('/', get_massage)
])


if __name__ == "__main__":
    web.run_app(
        host="0.0.0.0",
        port=environ.get("PORT_SEVICE"),
        app=app
        )
