import argon2
from dependency_injector import providers, containers

from access_service.application.usecases.create_user import CreateUser
from access_service.application.usecases.authorize import Authorize
from access_service.application.usecases.update_access_token import UpdateAccessToken

from access_service.infrastructure.repository.user import UserRepositoryImpl
from access_service.infrastructure.persistence.database import (
    get_async_engine,
    get_async_sessionmaker,
    get_async_session,
)
from access_service.infrastructure.services.auth.password_hasher import PasswordHasherImpl
from access_service.bootstrap.config import load_access_service_config

from access_service.presentation.auth.token_auth import TokenAuth
from access_service.infrastructure.services.auth.web_token_processor import WebTokenProcessor


from access_service.infrastructure.services.web_token.jwt_processor import JWTProcessorImpl


class ConfigContainer(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(
    #     modules=[
    #         "access_service.infrastructure.persistence.alembic.migrations.env",
    #     ],
    # )

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

class InfrastructureContainer(containers.DeclarativeContainer):

    config = providers.Container(ConfigContainer)
    db = providers.Container(DatabaseContainer)

    user_repository = providers.Singleton(
        UserRepositoryImpl,
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

class PresentationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "access_service.presentation.routes",
        ],
    )
    config = providers.Container(ConfigContainer) # Declare dependency on config
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
        user_repository=infrastructure.user_repository,
        password_hasher=infrastructure.password_hasher
    )
    authorize = providers.Singleton(
        Authorize,
        user_repository=infrastructure.user_repository,
        password_hasher=infrastructure.password_hasher,
        access_token_config=config.container.config.provided.access_token,
        refresh_token_config=config.container.config.provided.refresh_token,
    )
    update_access_token = providers.Singleton(
        UpdateAccessToken,
        access_token_config=config.container.config.provided.access_token,
    )

# class DatabaseContainer(containers.DeclarativeContainer):
#     # config = providers.DependenciesContainer()
#     config = providers.Container(ConfigContainer)

#     async_engine = providers.Resource(
#         get_async_engine,
#         settings=config.container.config.provided.db 
#     )
#     async_sessionmaker = providers.Resource(
#         get_async_sessionmaker,
#         async_engine=async_engine,
#     )
#     async_session = providers.Resource(
#         get_async_session,
#         async_sessionmaker=async_sessionmaker,
#     )

# class InfrastructureContainer(containers.DeclarativeContainer):

#     config = providers.Container(ConfigContainer)
#     db = providers.Container(DatabaseContainer)

#     user_repository = providers.Singleton(
#         UserRepositoryImpl,
#         session=db.async_session,
#     )
#     password_hasher = providers.Singleton(
#         PasswordHasherImpl,
#         password_hasher=argon2.PasswordHasher(),
#     )
#     jwt_processor = providers.Singleton(
#         JWTProcessorImpl,
#         config=config.container.config.provided.jwt
#     )
#     web_token_processor = providers.Singleton(
#         WebTokenProcessor,
#         jwt_processor=jwt_processor,
#     )

# class PresentationContainer(containers.DeclarativeContainer):
#     wiring_config = containers.WiringConfiguration(
#         packages=[
#             "access_service.presentation.routes",
#         ],
#     )
#     config = providers.Container(ConfigContainer) 
#     infrastructure = providers.DependenciesContainer()  
    

#     token_auth = providers.Singleton(
#         TokenAuth,
#         token_processor=infrastructure.web_token_processor,
#         config=config.container.config.provided.token_auth
#     )


# class ApplicationContainer(containers.DeclarativeContainer):
#     wiring_config = containers.WiringConfiguration(
#         packages=[
#             "access_service.presentation.routes",
#         ],
#     )

#     config = providers.Container(ConfigContainer)
#     infrastructure = providers.Container(InfrastructureContainer)

#     create_user = providers.Singleton(
#         CreateUser,
#         user_repository=infrastructure.user_repository,
#         password_hasher=infrastructure.password_hasher
#     )
#     authorize = providers.Singleton(
#         Authorize,
#         user_repository=infrastructure.user_repository,
#         password_hasher=infrastructure.password_hasher,
#         access_token_config=config.container.config.provided.access_token,
#         refresh_token_config=config.container.config.provided.refresh_token,
#     )
#     update_access_token = providers.Singleton(
#         UpdateAccessToken,
#         access_token_config=config.container.config.provided.access_token,
#     )
# class WebContainers:
#     application: ApplicationContainer
#     presentation: PresentationContainer


def setup_containers() -> None:
    config = ConfigContainer()
    db = DatabaseContainer()
    infrastructure = InfrastructureContainer()
    presentation = PresentationContainer()
    application = ApplicationContainer()

    # db.config.override(config.config)
    # infrastructure.config.override(config.config)  # Inject config into InfrastructureContainer
    # infrastructure.db.override(db)

    # application.config.override(config.config)  # Inject config into ApplicationContainer
    # application.infrastructure.override(infrastructure) 

    # presentation.config.override(config.config)  # Inject config into PresentationContainer
    # presentation.infrastructure.override(infrastructure)

    # config.wire()
    # db.wire()
    # infrastructure.wire()
    # presentation.wire()
    # application.wire()

    # config.config()  
    
    # db.async_engine()
    # db.async_sessionmaker()
    # db.async_session()  
   
    # infrastructure.user_repository()  
    # infrastructure.password_hasher()  
    # infrastructure.jwt_processor()  
    # infrastructure.web_token_processor()  

    # application.create_user()  
    # application.authorize()  
    # application.update_access_token() 
    
    # presentation.token_auth() 

    # return WebContainers(
    #     application=application,
    #     presentation=presentation,
    # )
