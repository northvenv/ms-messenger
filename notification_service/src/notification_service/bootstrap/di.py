from dependency_injector import containers, providers
from smsaero import SmsAero
from notification_service.message_broker.kafka import get_consumer, get_producer
from notification_service.bootstrap.config import load_notification_service_config
from notification_service.message_broker.kafka import KafkaMessageBroker
from notification_service.sms_sender.sms import SmsSender, get_sms_api


class ConfigContainer(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(
    #     modules=[
    #         "notification_service.lifespan",
    #     ],
    # )
    config = providers.Singleton(
        load_notification_service_config
    )

class KafkaContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "notification_service.main",
        ],
    )
    config = providers.DependenciesContainer()

    kafka_consumer = providers.Singleton(
        get_consumer,
        config=config.config.provided.kafka,
    )

    kafka_producer = providers.Singleton(
        get_producer,
        config=config.config.provided.kafka
    )

    message_broker = providers.Singleton(
        KafkaMessageBroker,
        consumer=kafka_consumer,
        producer=kafka_producer
    )

class SmsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "notification_service.lifespan",
        ],
    )
    config = providers.DependenciesContainer()

    sms_api = providers.Singleton(
        get_sms_api,
        config=config.config.provided.sms
    )
    sms_sender = providers.Singleton(
        SmsSender,
        sms_api=sms_api
    )


def setup_containers() -> ConfigContainer:
    config = ConfigContainer()

    kafka = KafkaContainer(config=config)
    sms = SmsContainer(config=config)

    return config
