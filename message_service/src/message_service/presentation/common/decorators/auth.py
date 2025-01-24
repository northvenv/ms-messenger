from functools import wraps
import socketio
from fastapi import Request
from dependency_injector.wiring import Provide, inject

from message_service.bootstrap.di import PresentationContainer

from message_service.domain.values.chat import UserId

def get_headers_from_scope(scope):
    headers = {}
    for header in scope['headers']:
        headers[header[0].decode('utf-8')] = header[1].decode('utf-8')
    return headers

def user_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            request = kwargs["request"]
        except KeyError:
            request = None

        try:
            environ = args[1] 
        except:
            environ = None

            
        if request:
            user_id = request.headers.get('Authorization')
            if not user_id:
                raise Exception("User_id is None")
            kwargs['user_id'] = user_id

        elif environ:
            headers = environ["asgi.scope"]["headers"]
            headers = {key.decode('utf-8'): value.decode('utf-8') for key, value in headers}

            user_id = headers.get('authorization')

            if not user_id:
                raise Exception("User_id is None")
            kwargs['user_id'] = user_id

        return await func(*args, **kwargs)
    
    return wrapper
            
        

        

