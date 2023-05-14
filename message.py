from aiohttp import web
from dotenv import load_dotenv
from os import environ
import json
from global_utils import HEADERS
load_dotenv()

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
        host=environ.get("HOST_MASSAGE"),
        port=environ.get("PORT_MASSAGE"),
        app=app
        )
