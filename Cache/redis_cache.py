from typing import Optional
from .base_class import BaseCache
import redis

class RedisCache(BaseCache):
    def __init__(self,
                 host: str = "localhost",
                 port: int = 6379,
                 db: int = 0,
                 ttl: int = 3600
                 ):
                 self.client = redis.Redis(host=host,
                 port=port,
                 db=db,
                 decode_responses=True)

                 self.ttl = ttl

    def _make_key(self, cache_key: str) -> str:
        return f"llm-cache{cache_key}"

    def check_connection(self)->bool:
        return self.client.ping()
    
    def get(self, cache_key: str) -> Optional[str]:
        return self.client.get(
            self._make_key(cache_key)
        )
    
    def set(self,
            cache_key: str,
            prompt: str,
            model_name: str,
            response: str):
            self.client.set(
                name=self._make_key(cache_key),
                value=response,
                ex=self.ttl
            )

    def clear(self):
        self.client.flushdb()

    def count(self):
        return self.client.dbsize()





