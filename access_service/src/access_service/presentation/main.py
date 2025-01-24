import logging
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiojobs import Scheduler
from typing import Callable
from access_service.presentation.routes.user import router as auth_router
from access_service.presentation.routes.token import router as token_router
from access_service.bootstrap.di import setup_containers
from fastapi.middleware.cors import CORSMiddleware
from access_service.presentation.lifespan import (
    init_message_broker, 
    close_message_broker,
    consume_sms_results_in_background
)
from dependency_injector.wiring import inject, Provide
from access_service.infrastructure.message_broker.kafka import KafkaMessageBroker
from access_service.bootstrap.di import (
    KafkaContainer,
    InfrastructureContainer
)
from access_service.bootstrap.config import AccessServiceConfig
from access_service.application.common.gateway.verification_token import VerificationTokenGateway


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
   

@inject
def custom_lifespan(
    config: AccessServiceConfig,
    message_broker: KafkaMessageBroker = Provide[KafkaContainer.message_broker],
    verification_token_gateway: VerificationTokenGateway = Provide[InfrastructureContainer.verification_token_gateway],
) -> Callable:
    @asynccontextmanager
    async def lifespan(
        app: FastAPI,
    ):
        await message_broker.start()
        scheduler = Scheduler()
        job = await scheduler.spawn(
            consume_sms_results_in_background(
                message_broker=message_broker,
                config=config,
                verification_token_gateway=verification_token_gateway
            )
        )
        yield
        await job.close()
        await message_broker.stop()
    
    return lifespan


def create_app() -> FastAPI:
    config = setup_containers()
    app = FastAPI(
        lifespan=custom_lifespan(
            config=config.config()
        )
    )
    
    app.include_router(auth_router)
    app.include_router(token_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


