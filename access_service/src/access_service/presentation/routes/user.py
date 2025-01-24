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
from access_service.application.usecases.send_verification_token import (
    SendVerificationToken,
    SendVerificationTokenInputDTO,
)
from access_service.application.usecases.update_access_token import UpdateAccessToken
from access_service.application.dto.user import UserDTO

from access_service.presentation.schemas.user import (
    CreateUserSchema,
    LoginSchema,
    SendVerificationSchema,
    VerificationSchema
)
from access_service.presentation.auth.token_auth import TokenAuthGateway

from access_service.bootstrap.di import (
    ApplicationContainer,
    PresentationContainer,
)
from access_service.application.usecases.verify_user import VerifyUser, VerificationInputDTO


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/signup")
@inject
async def create_user(
    data: CreateUserSchema,
    create_user: CreateUser = Depends(Provide[ApplicationContainer.create_user]),
) -> UserDTO:
    response = await create_user(
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
    token_auth: TokenAuthGateway = Depends(Provide[PresentationContainer.token_auth])
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


@router.post("/send_verification_token")
@inject
async def send_verification_token(
    data: SendVerificationSchema,
    send_verification_token: SendVerificationToken = Depends(Provide[ApplicationContainer.send_verification_token])
):
    await send_verification_token(
        SendVerificationTokenInputDTO(
            user_id=data.uid,
            phone_number=data.phone_number
        )
    )

@router.post("/verify")
@inject
async def verify_user(
    data: VerificationSchema,
    verify_user: VerifyUser = Depends(Provide[ApplicationContainer.verify_user])
):
    await verify_user(
        VerificationInputDTO(
            uid=data.uid,
            code=data.code
        )
    )





    

   

   

