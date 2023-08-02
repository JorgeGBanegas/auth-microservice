# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Union
from fastapi import APIRouter, Depends, Header
from app.schemas.auth.auth_schemas import (UserLoginSchema, UserSignupSchema,
                                           UserCognitoNewPasswordGetSchema, UserCognitoLoginSchema,
                                           UserCognitoNewPasswordSchema, UserSchema,
                                           UserUpdateImageSchema, UserCognitoSignupSchema)
from app.controllers.auth_controller import AuthController

router = APIRouter()

# Inicio de sesion con aws cognito


@router.post("/login")
def login(user: UserLoginSchema, auth_controller:
          AuthController = Depends()) -> Union[UserCognitoLoginSchema,
                                               UserCognitoNewPasswordSchema]:
    return auth_controller.signin(user)


@router.post("/signup")
def signup(user: UserSignupSchema, auth_controller:
           AuthController = Depends()) -> UserCognitoSignupSchema:
    return auth_controller.signup(user)


@router.post("/new-password")
def request_new_password(user: UserCognitoNewPasswordGetSchema,
                         auth_controller: AuthController = Depends()) -> UserCognitoLoginSchema:
    return auth_controller.first_signin(user)

# pylint: disable=invalid-name


def verify_access_token(Authorization: str = Header(None),
                        auth_controller: AuthController = Depends()):
    return auth_controller.verify_access_token(Authorization)


@router.post("/signout")
def signout(access_token: str = Depends(verify_access_token),
            auth_controller: AuthController = Depends()):
    return auth_controller.signout(access_token)


@router.get("/user", response_model=UserSchema)
def get_user(access_token: str = Depends(verify_access_token),
             auth_controller: AuthController = Depends()) -> UserSchema:
    return auth_controller.get_user(access_token)


@router.put("/user/image")
def update_image(user: UserUpdateImageSchema,
                 auth_controller: AuthController = Depends()):
    return auth_controller.update_image_s3(user)
