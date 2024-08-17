from aiohttp import web
import aiohttp_cors
from routes import setup_routes
from db import init_db


app = web.Application()
cors = aiohttp_cors.setup(app)


setup_routes(app)

for route in list(app.router.routes()):
    cors.add(route)


@app.on_startup.append
async def startup(*args):
    await init_db()

if __name__ == '__main__':
    web.run_app(app, port=8080)
