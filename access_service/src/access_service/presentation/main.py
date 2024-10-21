import logging
from fastapi import FastAPI


from access_service.presentation.routes.user import router as auth_router
from access_service.bootstrap.di import setup_containers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI()
    setup_containers()
    app.include_router(
        auth_router, 
        # dependencies=[
        #     Depends(lambda: web_containers.application),
        #     Depends(lambda: web_containers.presentation),
        # ]
    )

    return app

# if __name__ == "__main__":
#     import uvicorn
#     app = create_app()
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

