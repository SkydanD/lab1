from aiohttp import ClientSession

HEADERS = {'content-type': 'application/json'}


async def request_to_server(host: str, port: int, method: str, json: dict = {}, url: str = "/") -> dict:
    async with ClientSession(f"http://{host}:{port}") as session:
        async with session.request(url=url, method=method, json=json) as response:
            response.raise_for_status()
            return (await response.json())["Response"]
