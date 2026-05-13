from aiohttp import ClientSession
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, text

from app.db.models.cities import City
from app.services.coordinates import get_city_coordinates


async def city_check(city_name: str, db: AsyncSession) -> dict:
    res = await db.execute(
        select(City).where(City.name == city_name)
    )

    city = res.scalar_one_or_none()
    if city is None:
        raise HTTPException(status_code=404, detail=f"City {city_name} not found")

    return {
        "City": city.name,
        "Lat": city.lat,
        "Lon": city.lon
    }

async def two_cities(lat: float, lon: float, db: AsyncSession):
    haversine_sql = text("""
        SELECT *,
               (6371 * acos(cos(radians(:lat)) * 
                            cos(radians(cities.lat)) * 
                            cos(radians(cities.lon) - radians(:lon)) + 
                        sin(radians(:lat)) * sin(radians(cities.lat)))) AS distance_km
        FROM cities
        ORDER BY distance_km ASC
        LIMIT 2
    """)

    result = await db.execute(haversine_sql, {"lat": lat, "lon": lon})
    cities_with_dist = result.mappings().all()

    cities = []
    for row in cities_with_dist:
        city = City(id=row['id'], name=row['name'], lat=row['lat'], lon=row['lon'])
        city.distance_km = row['distance_km']
        cities.append(city)

    return cities

async def append_city(city_name: str, db: AsyncSession, http_session: ClientSession):
    res = await db.execute(select(City).where(City.name == city_name))
    city = res.scalar_one_or_none()
    if city:
        raise HTTPException(status_code=404, detail=f"City {city_name} already exists")

    res = await get_city_coordinates(city_name, http_session)
    if res is None:
        raise HTTPException(status_code=404, detail=f"City {city_name} not found")

    await db.execute(insert(City).values(name=city_name, lat=res["lat"], lon=res["lon"]))
    await db.commit()
    return {
        "Success": True,
        "City": city_name,
        "Latitude": res["lat"],
        "Longitude": res["lon"],
        "Description": f"City {city_name} successfully added"
    }


async def del_city(city_name: str, db: AsyncSession):
    result = await db.execute(delete(City).where(City.name == city_name))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail=f'City {city_name} not in db')

    await db.commit()
    return {
        "Success": True,
        "City": city_name,
        "Description": f"City {city_name} successfully deleted"
    }