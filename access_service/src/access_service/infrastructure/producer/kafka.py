from aiokafka import AIOKafkaProducer
from access_service.infrastructure.producer.config import KafkaConfig


def create_kafka_producer(settings: KafkaConfig) -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=settings.kafka_url
    )