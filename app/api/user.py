from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession

from app.services.user import city_check, two_cities, append_city, del_city
from app.db.session import get_db
from app.api.dependencies import get_http_session
from app.schemas.base import City


router= APIRouter()

@router.get("/info/{city_name}")
async def city_info(city_name: str, db: AsyncSession = Depends(get_db)):
    return await city_check(city_name, db)

@router.get("/nearest_cities")
async def two_nearest_cities(lat: float, lon:float, db: AsyncSession = Depends(get_db)):
    return await two_cities(lat, lon, db)

@router.post("/add")
async def add_city(city: City, db: AsyncSession = Depends(get_db), http_session: ClientSession = Depends(get_http_session)):
    return await append_city(city.city_name, db, http_session)

@router.delete("/delete")
async def delete_city(city: City, db: AsyncSession = Depends(get_db)):
    return await del_city(city.city_name, db)