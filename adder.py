import aiohttp
import asyncio

API_URL = 'http://localhost:8080/cities'

cities = [
    {
        "name": "Москва",
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    {
        "name": "Санкт-Петербург",
        "latitude": 59.9343,
        "longitude": 30.3351
    },
    {
        "name": "Новосибирск",
        "latitude": 55.0084,
        "longitude": 82.9357
    },
    {
        "name": "Екатеринбург",
        "latitude": 56.8389,
        "longitude": 60.6057
    },
    {
        "name": "Нижний Новгород",
        "latitude": 56.3269,
        "longitude": 44.0059
    }
]


async def add_city(session, city):
    async with session.post(API_URL, json=city) as response:
        if response.status == 200:
            print(f"Successfully added city: {city['name']}")
        else:
            result = await response.json()
            print(f"Failed to add city: {city['name']} - {result['error']}")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [add_city(session, city) for city in cities]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
