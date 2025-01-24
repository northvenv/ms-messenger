# import uvicorn
# import asyncio

# from message_service.presentation.rest.main import create_app
# from message_service.presentation.websocket.main import create_socket_app
# from message_service.bootstrap.di import setup_containers



# async def main():
#     fastapi_config = uvicorn.Config(create_app(), host="0.0.0.0", port=8001, reload=True)
#     socketio_config = uvicorn.Config(create_socket_app(), host="0.0.0.0", port=8002, reload=True)

#     fastapi_server = uvicorn.Server(fastapi_config)
#     socketio_server = uvicorn.Server(socketio_config)

#     await asyncio.gather(
#         fastapi_server.serve(),
#         socketio_server.serve()
#     )

#     setup_containers()

# if __name__ == "__main__":
#     asyncio.run(main())  