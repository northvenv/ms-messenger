from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject


from access_service.application.usecases.update_access_token import UpdateAccessToken

from access_service.presentation.auth.token_auth import TokenAuthGateway

from access_service.bootstrap.di import (
    ApplicationContainer,
    PresentationContainer,
)
from access_service.application.dto.access_token import AccessTokenDTO


router = APIRouter(
    prefix="/token",
    tags=["Token"],
)


@router.post("/refresh")
@inject
async def refresh_token(
    request: Request,
    update_access_token: UpdateAccessToken = Depends(Provide[ApplicationContainer.update_access_token]),
    token_auth: TokenAuthGateway = Depends(Provide[PresentationContainer.token_auth]),
) -> Response:
    refresh_token = token_auth.get_refresh_token(request)

    access_token = await update_access_token(refresh_token)

    http_response = JSONResponse(status_code=201, content={})

    return token_auth.set_access_token(
        access_token_data=access_token,
        response=http_response,
    )

@router.get("/verify")
@inject
async def verify_token(
    request: Request,
    token_auth: TokenAuthGateway = Depends(Provide[PresentationContainer.token_auth]),
) -> Response:
    access_token = token_auth.get_access_token(request)

    headers = {
        "X-User-Uid": str(access_token.uid),
        "X-User-Expires-In": access_token.expires_in.isoformat(),
        "X-Token-Id": str(access_token.token_id)
    }

    return JSONResponse(content={"status": "verified"}, headers=headers)

