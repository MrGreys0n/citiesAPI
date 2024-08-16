import json
from aiohttp import web
from city_storage import CityStorage

storage = CityStorage()


def is_valid_coordinate(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return False

    return -90 <= lat <= 90 and -180 <= lon <= 180


async def add_city(request):
    try:
        data = await request.json()
        city_name = data.get('name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not city_name or latitude is None or longitude is None:
            return web.json_response({'error': 'City name, latitude, and longitude are required'}, status=400)

        if not is_valid_coordinate(latitude, longitude):
            return web.json_response({'error': 'Invalid coordinates'}, status=400)

        # Проверяем, существует ли уже город
        existing_city = storage.get_city(city_name)
        if existing_city is not None:
            return web.json_response({'error': f'City with name {city_name} already exists'}, status=400)

        # Добавляем новый город
        await storage.add_city(city_name, latitude, longitude)
        return web.json_response({'message': 'City added successfully'})
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON'}, status=400)
    except ValueError as e:
        return web.json_response({'error': str(e)}, status=400)


async def delete_city(request):
    city_name = request.match_info.get('city_name')
    await storage.delete_city(city_name)
    return web.json_response({'message': 'City deleted successfully'})


async def get_all_cities(request):
    cities = await storage.get_all_cities()
    return web.json_response(cities)


async def get_city(request):
    city_name = request.match_info.get('city_name')
    city = storage.get_city(city_name)
    if city is None:
        return web.json_response({'error': 'City not found'}, status=404)
    return web.json_response(city)


async def get_nearest_cities(request):
    try:
        latitude = float(request.query.get('latitude'))
        longitude = float(request.query.get('longitude'))
    except (TypeError, ValueError):
        return web.json_response({'error': 'Invalid latitude or longitude'}, status=400)

    if not is_valid_coordinate(latitude, longitude):
        return web.json_response({'error': 'Invalid coordinates'}, status=400)

    nearest_cities = await storage.get_nearest_cities(latitude, longitude)

    return web.json_response(nearest_cities)
