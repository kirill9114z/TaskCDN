from pydantic import BaseModel, Field, field_validator

class City(BaseModel):
    city_name: str = Field(..., max_length=168, min_length=1)

    @field_validator("city_name")
    @classmethod
    def city_name_validator(cls, v: str) -> str:
        if v.isdigit():
            raise ValueError("City name cannot have digits")

        v = ' '.join(v.split())

        if not v:
            raise ValueError("City name cannot be empty")
        return v


class Coordinates(BaseModel):
    lat: float
    lon: float

    @field_validator("lat")
    @classmethod
    def lat_validate(cls, lt: float) -> float:
        if abs(lt) > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return lt

    @field_validator("lon")
    @classmethod
    def lon_validate(cls, ln: float) -> float:
        if abs(ln) > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return ln

