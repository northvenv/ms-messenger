from abc import ABC, abstractmethod
from dataclasses import dataclass
from access_service.infrastructure.message_broker.base import BaseMessageBroker





class EventHandler[ET, ER](ABC):
    def __init__(
        self, 
        message_broker: BaseMessageBroker,
        broker_topic: str | None = None
    ):
        self.message_broker: BaseMessageBroker = message_broker
        self.broker_topic = broker_topic

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...