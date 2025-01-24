import socketio

from typing import Optional
from dependency_injector.wiring import Provide, inject


from message_service.application.usecase.get_chat import (
    GetChat,
    GetChatInputDTO,
)

from message_service.bootstrap.di import ApplicationContainer
from message_service.presentation.common.decorators.auth import user_auth
from message_service.bootstrap.di import ApplicationContainer
from message_service.application.usecase.send_message import (
    SendMessage,
    SendMessageInputDTO
)
from message_service.presentation.common.decorators.auth import user_auth

from message_service.presentation.websocket.utils.converter import (
    convert_dataclass_to_json,
    convert_string_to_dict
)
from message_service.presentation.websocket.utils.validator import (
    validate_chat_dict,
    validate_message_dict
)


sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode="asgi")


@sio.event
@user_auth
async def connect(sid, environ, user_id: str = None):
    await sio.save_session(sid, {'uid': user_id})


@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")


@sio.event
@inject
async def join_chat(
    sid, 
    data,
    get_chat: GetChat = Provide[ApplicationContainer.get_chat],
    user_id: str = None
):
    session = await sio.get_session(sid)
    data_dict = convert_string_to_dict(data)
    chat_data = validate_chat_dict(data_dict)

    chat = await get_chat(
        GetChatInputDTO(
            chat_id=chat_data.chat_id,
            user_id=session["uid"],
        )
    )
    await sio.enter_room(sid, chat_data.chat_id)
    await sio.emit('message', {'message': 'User connect to chat!'}, room=chat_data.chat_id)

    chat_json = convert_dataclass_to_json(chat)
    await sio.emit('chat_data', chat_json, room=chat_data.chat_id)


@sio.event
@inject
async def send_message(
    sid, 
    data,  
    send_message: SendMessage = Provide[ApplicationContainer.send_message],  
    user_id: Optional[str] = None
):
    session = await sio.get_session(sid)
    user_id = session.get("uid", user_id)  

    data_dict = convert_string_to_dict(data)
    message_data = validate_message_dict(data_dict)

    message = await send_message(
        SendMessageInputDTO(
            chat_id=message_data.chat_id,
            sender_id=user_id,
            message_body=message_data.message_body,
        )
    )
    message_json = convert_dataclass_to_json(message)
    await sio.emit('new_message', message_json, room=message_data.chat_id)





























# @router.websocket("/{chat_oid}/")
# async def websocket_endpoint(
#     chat_id: str,
#     websocket: WebSocket,
#     container: Container = Depends(init_container),
#     get_chat: GetChat = ...
# ):
#     connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)

#     try:
#         await get_chat(GetChatInputDTO(chat_id=chat_id))
#     except ChatNotFoundException as error:
#         await websocket.accept()
#         await websocket.send_json(data={'error': error.message})
#         await websocket.close()
#         return

#     await connection_manager.accept_connection(websocket=websocket, key=chat_id)

#     await websocket.send_text("You are connected!")

#     try:
#         while True:
#             await websocket.receive_text()

#     except WebSocketDisconnect:
#         await connection_manager.remove_connection(websocket=websocket, key=chat_id)
