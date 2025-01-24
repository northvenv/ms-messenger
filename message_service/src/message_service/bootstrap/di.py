from dependency_injector import containers, providers

from message_service.bootstrap.config import load_message_service_config

from message_service.application.usecase.create_chat import CreateChat
from message_service.application.usecase.get_chat import GetChat
from message_service.application.usecase.send_message import SendMessage

from message_service.infrastructure.persistence.mongo import get_mongo_client
from message_service.infrastructure.repositories.chat import ChatRepositoryImpl
from message_service.infrastructure.repositories.message import MessageRepositoryImpl


class ConfigContainer(containers.DeclarativeContainer):
    config = providers.Singleton(
        load_message_service_config
    )
    

class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.DependenciesContainer()

    mongo_client = providers.Singleton(
        get_mongo_client, 
        settings=config.config.provided.mongo_db_config
    )
    chat_repository = providers.Singleton(
        ChatRepositoryImpl,
        mongo_client=mongo_client,
        config=config.config.provided.mongo_db_config,
    )
    message_repository = providers.Singleton(
        MessageRepositoryImpl,
        mongo_client=mongo_client,
        config=config.config.provided.mongo_db_config,
    )

class PresentationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "message_service.presentation",
        ],
    )
    config = providers.DependenciesContainer()
    infrastructure = providers.Container(InfrastructureContainer, config=config)



class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "message_service.presentation.rest.routes",
            "message_service.presentation.websocket.routes",
        ],
    )
    config = providers.DependenciesContainer()
    infrastructure = providers.Container(InfrastructureContainer, config=config)

    create_chat = providers.Factory(
        CreateChat,
        chat_repository=infrastructure.chat_repository
    )
    get_chat = providers.Factory(
        GetChat,
        chat_repository=infrastructure.chat_repository,
        message_repository=infrastructure.message_repository,
    )
    send_message = providers.Factory(
        SendMessage,
        message_repository=infrastructure.message_repository,
        chat_repository=infrastructure.chat_repository
    )

def setup_containers():
    config = ConfigContainer()

    infrastructure = InfrastructureContainer(config=config)
    application = ApplicationContainer(config=config)
    presentation = PresentationContainer(config=config)

    return config, infrastructure, application, presentation