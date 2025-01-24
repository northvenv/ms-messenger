import argon2
from dependency_injector import providers, containers
from aiokafka import AIOKafkaProducer

from access_service.application.usecases.create_user import CreateUser
from access_service.application.usecases.authorize import Authorize
from access_service.application.usecases.update_access_token import UpdateAccessToken
from access_service.application.usecases.send_verification_token import SendVerificationToken

from access_service.infrastructure.gateway.user import UserGatewayImpl
from access_service.infrastructure.persistence.database import (
    get_async_engine,
    get_async_sessionmaker,
    get_async_session,
)
from access_service.infrastructure.services.auth.password_hasher import PasswordHasherImpl
from access_service.bootstrap.config import load_access_service_config

from access_service.presentation.auth.token_auth import TokenAuthGateway
from access_service.infrastructure.services.auth.web_token_processor import WebTokenProcessor
from access_service.infrastructure.cache.redis import (
    get_redis_pool,
    get_redis_session,
)
from access_service.infrastructure.web_token.jwt_processor import JWTProcessorImpl
from access_service.infrastructure.events.verification_token import VerificationTokenCreatedEventHandler
from access_service.infrastructure.message_broker.kafka import (
    KafkaMessageBroker, 
    get_producer,
    get_consumer
)
from access_service.infrastructure.gateway.verification_token import VerificationTokenGatewayImpl
from access_service.bootstrap.config import AccessServiceConfig
from access_service.application.usecases.verify_user import VerifyUser


class ConfigContainer(containers.DeclarativeContainer):
    config = providers.Singleton(
        load_access_service_config
    )

class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.DependenciesContainer()

    async_engine = providers.Resource(
        get_async_engine,
        settings=config.config.provided.db,
    )
    session_factory = providers.Resource(
        get_async_sessionmaker,
        async_engine=async_engine,
    )
    async_session = providers.Resource(
        get_async_session,
        session_factory=session_factory,
    )

class RedisContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "access_service.presentation.lifespan",
        ],
    )
    config = providers.DependenciesContainer()

    redis_pool = providers.Singleton(
        get_redis_pool,
        settings=config.config.provided.redis
    )

    redis_session = providers.Factory(
        get_redis_session,
        pool=redis_pool
    )

class KafkaContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "access_service.presentation.main",
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
        producer=kafka_producer,
        consumer=kafka_consumer
    )

class InfrastructureContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "access_service.presentation.main",
        ],
    )
    config = providers.DependenciesContainer()
    db = providers.Container(DatabaseContainer, config=config)
    redis = providers.Container(RedisContainer, config=config)


    user_gateway = providers.Singleton(
        UserGatewayImpl,
        session=db.async_session,
    )
    verification_token_gateway = providers.Singleton(
        VerificationTokenGatewayImpl,
        session=redis.redis_session
    )
    password_hasher = providers.Singleton(
        PasswordHasherImpl,
        password_hasher=argon2.PasswordHasher(),
    )
    jwt_processor = providers.Singleton(
        JWTProcessorImpl,
        config=config.config.provided.jwt
    )
    web_token_processor = providers.Singleton(
        WebTokenProcessor,
        jwt_processor=jwt_processor,
    )


class PresentationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "access_service.presentation.main",
            "access_service.presentation.routes.user",
            "access_service.presentation.routes.token",
        ],
    )
    config = providers.DependenciesContainer()
    infrastructure = providers.Container(InfrastructureContainer, config=config)
    
    token_auth = providers.Singleton(
        TokenAuthGateway,
        token_processor=infrastructure.web_token_processor,
        config=config.config.provided.token_auth
    )


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "access_service.presentation.main",
            "access_service.presentation.routes.user",
            "access_service.presentation.routes.token",
        ],
    )

    config = providers.DependenciesContainer()
    infrastructure = providers.Container(InfrastructureContainer, config=config)
    kafka = providers.Container(KafkaContainer, config=config)

    verification_token_created_event_handler = providers.Singleton(
        VerificationTokenCreatedEventHandler,
        message_broker=kafka.message_broker,
        broker_topic=config.config.provided.kafka.verification_token_topic
    )
    create_user = providers.Singleton(
        CreateUser,
        user_gateway=infrastructure.user_gateway,
        password_hasher=infrastructure.password_hasher
    )
    authorize = providers.Singleton(
        Authorize,
        user_gateway=infrastructure.user_gateway,
        password_hasher=infrastructure.password_hasher,
        access_token_config=config.config.provided.access_token,
        refresh_token_config=config.config.provided.refresh_token,
    )
    update_access_token = providers.Singleton(
        UpdateAccessToken,
        access_token_config=config.config.provided.access_token,
    )
    send_verification_token = providers.Singleton(
        SendVerificationToken,
        verification_token_config=config.config.provided.verification_token,
        verification_token_created_event_handler=verification_token_created_event_handler
    )
    verify_user = providers.Singleton(
        VerifyUser,
        user_gateway=infrastructure.user_gateway,
        verification_token_gateway=infrastructure.verification_token_gateway
    )


def setup_containers() -> AccessServiceConfig:
    config = ConfigContainer()

    redis = RedisContainer(config=config)
    kafka = KafkaContainer(config=config)
    infrastructure = InfrastructureContainer(config=config)
    presentation = PresentationContainer(config=config)
    application = ApplicationContainer(config=config)

    return config




