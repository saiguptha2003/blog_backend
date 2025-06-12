import redis
import os
from app.utils.logger import logger

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True  # This will decode the responses from bytes to str
)

def get_redis_client():
    try:
        redis_client.ping()
        return redis_client
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise e
