import argon2
from dependency_injector import providers, containers

from access_service.application.usecases.create_user import CreateUser
from access_service.application.usecases.authorize import Authorize
from access_service.application.usecases.update_access_token import UpdateAccessToken
from access_service.application.usecases.send_verification_token import SendVerificationToken

from access_service.infrastructure.gateway.user import UserGatewayImpl
from access_service.infrastructure.gateway.verification_token import VerificationTokenGatewayImpl

from access_service.infrastructure.persistence.database import (
    get_async_engine,
    get_async_sessionmaker,
    get_async_session,
)
from access_service.infrastructure.services.auth.password_hasher import PasswordHasherImpl
from access_service.bootstrap.config import load_access_service_config

from access_service.presentation.auth.token_auth import TokenAuth
from access_service.infrastructure.services.auth.web_token_processor import WebTokenProcessor
from access_service.infrastructure.cache.redis import (
    get_redis_pool,
    get_redis_session,
)
from access_service.infrastructure.services.web_token.jwt_processor import JWTProcessorImpl
from access_service.infrastructure.producer.kafka import create_kafka_producer


class ConfigContainer(containers.DeclarativeContainer):
    config = providers.Singleton(
        load_access_service_config
    )

class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Container(ConfigContainer)

    async_engine = providers.Resource(
        get_async_engine,
        settings=config.container.config.provided.db,
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
    config = providers.Container(ConfigContainer)

    redis_pool = providers.Resource(
        get_redis_pool,
        settings=config.container.config.provided.redis
    )

    redis_session = providers.Resource(
        get_redis_session,
        pool=redis_pool
    )

class KafkaContainer(containers.DeclarativeContainer):
    config = providers.Container(ConfigContainer)

    create_kafka_producer = providers.Resource(
        create_kafka_producer,
        settings=config.container.config.provided.kafka,
    )

class InfrastructureContainer(containers.DeclarativeContainer):

    config = providers.Container(ConfigContainer)
    db = providers.Container(DatabaseContainer)
    redis = providers.Container(RedisContainer)
    kafka = providers.Container(KafkaContainer)


    user_gateway = providers.Singleton(
        UserGatewayImpl,
        session=db.async_session,
    )
    password_hasher = providers.Singleton(
        PasswordHasherImpl,
        password_hasher=argon2.PasswordHasher(),
    )
    jwt_processor = providers.Singleton(
        JWTProcessorImpl,
        config=config.container.config.provided.jwt
    )
    web_token_processor = providers.Singleton(
        WebTokenProcessor,
        jwt_processor=jwt_processor,
    )
    verification_token_gateway = providers.Singleton(
        VerificationTokenGatewayImpl,
        topic="verification_topic",
        producer=kafka.create_kafka_producer,
        redis=redis.redis_session
    )


class PresentationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "access_service.presentation.routes",
        ],
    )
    config = providers.Container(ConfigContainer) 
    infrastructure = providers.Container(InfrastructureContainer)
    
    token_auth = providers.Singleton(
        TokenAuth,
        token_processor=infrastructure.web_token_processor,
        config=config.container.config.provided.token_auth
    )


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "access_service.presentation.routes.user",
        ],
    )

    config = providers.Container(ConfigContainer) 
    infrastructure = providers.Container(InfrastructureContainer)

    create_user = providers.Singleton(
        CreateUser,
        user_gateway=infrastructure.user_gateway,
        password_hasher=infrastructure.password_hasher
    )
    authorize = providers.Singleton(
        Authorize,
        user_gateway=infrastructure.user_gateway,
        password_hasher=infrastructure.password_hasher,
        access_token_config=config.container.config.provided.access_token,
        refresh_token_config=config.container.config.provided.refresh_token,
    )
    update_access_token = providers.Singleton(
        UpdateAccessToken,
        access_token_config=config.container.config.provided.access_token,
    )
    send_verification_token = providers.Singleton(
        SendVerificationToken,
        verification_token_gateway=infrastructure.verification_token_gateway,
        verification_token_config=config.container.config.provided.verification_token,
    )




def setup_containers() -> None:
    config = ConfigContainer()
    db = DatabaseContainer()
    infrastructure = InfrastructureContainer()
    presentation = PresentationContainer()
    application = ApplicationContainer()

