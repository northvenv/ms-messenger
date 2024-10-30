import orjson
from redis.asyncio import Redis
from redis.exceptions import RedisError
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from access_service.domain.entities.verification_token import VerificationToken
from access_service.infrastructure.gateway.converters.verification_token import convert_verification_token_entity_to_dict


class VerificationTokenGatewayImpl:
    def __init__(
        self,
        topic: str,
        producer: AIOKafkaProducer,
        redis: Redis,
    ):
        self.topic: str = topic
        self.producer: AIOKafkaProducer = producer
        self.redis: Redis = redis

    async def produce_verification_token(self, data: VerificationToken) -> None:
        await self.producer.start()
        try:
            data_dict = convert_verification_token_entity_to_dict(data)
            value_bytes = orjson.dumps(data_dict)
            await self.producer.send(
                topic=self.topic,
                value=value_bytes,
            )
        except KafkaError:
            raise KafkaError
        finally:
            await self.producer.stop()

    async def save_verification_token(self, data: VerificationToken) -> None:
        try:
            data_dict = convert_verification_token_entity_to_dict(data)
            token_id_bytes = orjson.dumps(data_dict["token_id"])
            metadata_bytes = orjson.dumps(data_dict["metadata"])

            await self.redis.set(
                name=token_id_bytes,
                value=metadata_bytes,
            )
        except RedisError:
            raise RedisError
    