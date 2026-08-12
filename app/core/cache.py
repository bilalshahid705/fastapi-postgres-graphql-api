import json
from redis.asyncio import Redis
from app.core.config import settings

print("settings.VALKEY_URL:", settings.VALKEY_URL)

redis_client = Redis.from_url(
    settings.VALKEY_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def get_cache(key: str):

    print(f"Getting cache for key: {key}")
    value = await redis_client.get(key)


    print(f"Getting cache for value: {value}")

    if value is None:
        return None

    return json.loads(value)


async def set_cache(
    key: str,
    value,
    expire: int = 60,
):
    await redis_client.set(
        key,
        json.dumps(value),
        ex=expire,
    )


async def delete_cache(key: str):
    await redis_client.delete(key)