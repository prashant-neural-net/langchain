from abc import ABC, abstractmethod
from typing import Optional

class BaseCache(ABC):

    @abstractmethod
    def get(self, cache_key: str)->str:
        pass

    @abstractmethod
    def set(self, cache_key: str, prompt: str, model_name: str, response: str):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def count(self):
        pass