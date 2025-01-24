import orjson

from typing import AsyncIterator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from access_service.infrastructure.message_broker.base import BaseMessageBroker
from access_service.infrastructure.message_broker.config import KafkaConfig


def get_producer(config: KafkaConfig):
    return AIOKafkaProducer(
        bootstrap_servers=config.url,
        request_timeout_ms=5000,  
        linger_ms=10
    )

def get_consumer(config: KafkaConfig):
    return AIOKafkaConsumer(
        bootstrap_servers=config.url,
        # group_id=f"notifications-{uuid4()}",
    )


class KafkaMessageBroker(BaseMessageBroker):
    def __init__(
        self,
        consumer: AIOKafkaConsumer,
        producer: AIOKafkaProducer
    ):
        self.consumer: AIOKafkaConsumer = consumer
        self.producer: AIOKafkaProducer = producer

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def stop(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def send_message(self, topic: str, value: bytes, key: bytes):
        await self.producer.start()
        await self.producer.send(
            topic=topic,
            value=value,
            key=key
        )

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)
        
    async def stop_consuming(self):
        self.consumer.unsubscribe()




