from fastapi import Response, Request


from access_service.infrastructure.services.auth.web_token_processor import (
    WebTokenProcessor,
    AccessTokenType,
    RefreshTokenType,
)
from access_service.application.dto.access_token import AccessTokenDTO
from access_service.application.dto.refresh_token import RefreshTokenDTO
from access_service.presentation.auth.config import TokenAuthConfig





class TokenAuth:
    def __init__(
        self,
        token_processor: WebTokenProcessor,
        config: TokenAuthConfig,
    ):
        self.token_processor: WebTokenProcessor = token_processor
        self.config: TokenAuthConfig = config

    def get_access_token(
        self,
        request: Request,
    ) -> AccessTokenDTO: 
        access_token = request.cookies.get(self.config.access_token_cookie_key)

        access_token_data = self.token_processor.decode(access_token, AccessTokenType)

        return access_token_data
    
    def get_refresh_token(
        self,
        request: Request
    ) -> RefreshTokenDTO: 
        refresh_token = request.cookies.get(self.config.access_token_cookie_key)
        refresh_token_data = self.token_processor.decode(refresh_token, RefreshTokenType)
        
        return refresh_token_data
    
    def _set_cookie(
        self, 
        token_data: AccessTokenDTO | RefreshTokenDTO,
        token_cookie_key: str,
        response: Response
    ) -> Response:
        token = self.token_processor.encode(token_data)
        response.set_cookie(token_cookie_key, token, httponly=True)

        return response
    
    def set_access_token(
        self, 
        access_token_data: AccessTokenDTO,
        response: Response,
    ) -> Response:
        response = self._set_cookie(access_token_data, self.config.access_token_cookie_key, response)

        return response
    
    def set_refresh_token(
        self,
        refresh_token_data: RefreshTokenDTO,
        response: Response,
    ) -> Response:
        response = self._set_cookie(refresh_token_data, self.config.refresh_token_cookie_key, response)

        return response

    def set_session(
        self, 
        access_token_data: AccessTokenDTO,
        refresh_token_data: RefreshTokenDTO,
        response: Response,
    ) -> Response:
        response = self.set_access_token(access_token_data, response)
        response = self.set_refresh_token(refresh_token_data, response)

        return response




