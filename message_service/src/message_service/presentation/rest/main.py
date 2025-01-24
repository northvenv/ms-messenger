import uvicorn
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from message_service.presentation.rest.routes.chat import router as chat_router
from message_service.presentation.rest.routes.message import router as message_router

from message_service.bootstrap.di import setup_containers

def create_app() -> FastAPI:
    app = FastAPI()
    setup_containers()

    app.include_router(router=chat_router)
    app.include_router(router=message_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app



