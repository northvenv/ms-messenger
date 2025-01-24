from abc import ABC, abstractmethod
from typing import AsyncIterator


class BaseMessageBroker(ABC):
    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        raise NotImplementedError

    @abstractmethod
    async def stop_consuming(self):
        raise NotImplementedError
    
    @abstractmethod
    async def send_message(self, key: str, topic: str, value: bytes):
        raise NotImplementedError

    @abstractmethod
    async def start(self):
        raise NotImplementedError

    @abstractmethod
    async def stop(self):
        raise NotImplementedError
        
