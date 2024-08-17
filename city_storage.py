from geopy.distance import geodesic
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import City
from db import async_session


class CityStorage:
    @staticmethod
    async def add_city(name, latitude, longitude):
        async with async_session() as session:
            new_city = City(name=name, latitude=latitude, longitude=longitude)
            session.add(new_city)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError(f'City with name {name} already exists')

    @staticmethod
    async def delete_city(name):
        async with async_session() as session:
            result = await session.execute(select(City).filter_by(name=name))
            city = result.scalars().first()
            if city:
                await session.delete(city)
                await session.commit()

    @staticmethod
    async def get_all_cities():
        async with async_session() as session:
            result = await session.execute(select(City))
            cities = result.scalars().all()
            return {city.name: {'latitude': city.latitude, 'longitude': city.longitude} for city in cities}

    @staticmethod
    async def get_city(name):
        async with async_session() as session:
            result = await session.execute(select(City).filter_by(name=name))
            city = result.scalars().first()
            if city:
                return {'latitude': city.latitude, 'longitude': city.longitude}
            return None

    async def get_nearest_cities(self, latitude, longitude, num_cities=2):
        cities = await self.get_all_cities()
        distances = []
        for city, coords in cities.items():
            distance = geodesic((latitude, longitude), (coords['latitude'], coords['longitude'])).kilometers
            distances.append((city, distance))
        distances.sort(key=lambda x: x[1])
        return distances[:num_cities]
