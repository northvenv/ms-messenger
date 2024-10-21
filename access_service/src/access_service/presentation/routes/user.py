from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from access_service.application.usecases.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from access_service.application.usecases.authorize import (
    Authorize,
    AuthorizeInputDTO,
)
from access_service.application.usecases.update_access_token import UpdateAccessToken
from access_service.application.dto.user import UserDTO

from access_service.bootstrap.di import (
    ApplicationContainer,
    PresentationContainer,
)

from access_service.presentation.schemas.user import (
    CreateUserSchema,
    LoginSchema,
)
from access_service.presentation.auth.token_auth import TokenAuth


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/signup")
@inject
async def create_user(
    data: CreateUserSchema,
    create_user_action: CreateUser = Depends(Provide[ApplicationContainer.create_user]),
) -> UserDTO:
    print(f"create_user_action type: {type(create_user_action)}")
    response = await create_user_action(
        CreateUserInputDTO(
            username=data.username,
            phone_number=data.phone_number,
            password=data.password,
        ),
    )
    return response


@router.post("/login")
@inject
async def login_user(
    data: LoginSchema,
    auth_action: Authorize = Depends(Provide[ApplicationContainer.authorize]),
    token_auth: TokenAuth = Depends(Provide[PresentationContainer.token_auth])
) -> Response:
    web_tokens = await auth_action(
        AuthorizeInputDTO(
            phone_number=data.phone_number,
            password=data.password,
        )
    )
    http_response = JSONResponse(status_code=201, content={})

    return token_auth.set_session(
        access_token_data=web_tokens.access_token,
        refresh_token_data=web_tokens.refresh_token,
        response=http_response
    )


@router.post("/refresh")
@inject
async def refresh_token(
    request: Request,
    update_access_token_action: UpdateAccessToken = Depends(Provide[ApplicationContainer.update_access_token]),
    token_auth: TokenAuth = Depends(Provide[PresentationContainer.token_auth]),
) -> Response:
    refresh_token = token_auth.get_refresh_token(request)

    access_token = await update_access_token_action(refresh_token)

    http_response = JSONResponse(status_code=201, content={})

    return token_auth.set_access_token(
        access_token_data=access_token,
        response=http_response,
    )
    

   

   

