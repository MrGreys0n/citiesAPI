from aiohttp import web
import aiohttp_cors
from routes import setup_routes
from db import init_db


async def suppress_invalid_requests_middleware(app, handler):
    async def middleware_handler(request):
        try:
            return await handler(request)
        except web.HTTPBadRequest as e:
            if "Invalid method encountered" in str(e):
                # Возвращаем пустой ответ с кодом 400, но не выводим ошибку в лог
                return web.Response(status=400)
            raise
        except Exception as e:
            # Здесь можно обработать и другие исключения, если нужно
            raise
    return middleware_handler

# Создаем приложение и добавляем middleware
app = web.Application(middlewares=[suppress_invalid_requests_middleware])
cors = aiohttp_cors.setup(app)

setup_routes(app)

for route in list(app.router.routes()):
    cors.add(route)


@app.on_startup.append
async def startup(app):
    await init_db()

if __name__ == '__main__':
    web.run_app(app, port=8080)
