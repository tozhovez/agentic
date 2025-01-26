import redis.asyncio as redis

class AsyncRedisLocalCacheClient:
    """A simple wrapper for a asyncio Redis client."""
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._pool = None

    async def connect(self):
        """Create a Redis connection pool."""
        if not self._pool:
            self._pool = redis.from_url(self.redis_url, decode_responses=True)

    async def set(self, key: str, value: str):
        """Set a value in Redis."""
        if not self._pool:
            raise RuntimeError("Redis connection not initialized. Call `connect` first.")
        await self._pool.set(key, value)

    async def get(self, key: str):
        """Get a value from Redis."""
        if not self._pool:
            raise RuntimeError("Redis connection not initialized. Call `connect` first.")
        return await self._pool.get(key)

    async def close(self):
        """Close the Redis connection."""
        if self._pool:
            await self._pool.close()
            self._pool = None

