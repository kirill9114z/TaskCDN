from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    BASE_URL: str

    MAX_RETRIES: int
    DELAY: int
    RETRY_STATUSES = {429, 500, 502, 503, 504}

    HEADERS = {
        "User-Agent": "YourAppName/1.0 (shurahtovlist_ru@bk.ru)"
    }
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL="postgresql+asyncpg://postgres:12345@localhost:5438/my_db",
        BASE_URL="https://nominatim.openstreetmap.org/search",
        MAX_RETRIES=3,
        DELAY=1,
    )

settings = get_settings()

