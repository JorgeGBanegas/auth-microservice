# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Union
from fastapi import Depends
from app.dependencies.dependencies import get_auth_service
from app.schemas.auth.auth_schemas import (UserLoginSchema, UserSignupSchema,
                                            UserCognitoLoginSchema, UserCognitoNewPasswordSchema,
                                            UserCognitoSignupSchema, UserSchema,
                                            UserUpdateImageSchema)
from app.services.auth_service import AuthService
from app.exceptions.auth_exceptions import (NotAuthorized, UserNotFound, InvalidCode,
                                            InvalidSession, TokenNotFound, TokenNotValid,
                                            InvalidPassword)


class AuthController :
    def __init__(self, auth_service: AuthService = Depends(get_auth_service)) -> None:
        self.auth_service = auth_service

    def signin(self, user: UserLoginSchema) -> Union[UserCognitoLoginSchema,
                                                    UserCognitoNewPasswordSchema]:
        return self.auth_service.signin(user)

    def signup(self, user: UserSignupSchema) -> UserCognitoSignupSchema:
        return self.auth_service.signup(user)

    def first_signin(self, user: UserLoginSchema) -> UserCognitoLoginSchema:
        try:
            return self.auth_service.first_signin(user)
        except InvalidCode as error:
            raise error
        except InvalidSession as error:
            raise error
        except InvalidPassword as error:
            raise error
        except Exception as error:
            raise error

    def signout(self, access_token: str) -> dict:
        return self.auth_service.signout(access_token)

    def verify_access_token(self, authorization) -> dict:
        try:
            if authorization is None:
                raise TokenNotFound()
            if not authorization.startswith("Bearer "):
                raise TokenNotValid()
            access_token = authorization.split(" ")[1]
            return access_token
        except TokenNotFound as error:
            raise error
        except TokenNotValid as error:
            raise error
        except Exception as error:
            raise error

    def get_user(self, access_token: str) -> UserSchema:
        try:
            return self.auth_service.get_user(access_token)
        except NotAuthorized as error:
            raise error
        except UserNotFound as error:
            raise error
        except Exception as error:
            raise error

    def save_image_to_s3(self, image: str) -> str:
        try:
            return self.auth_service.save_image_to_s3(image)
        except Exception as error:
            raise error

    def update_image_s3(self, user: UserUpdateImageSchema) -> str:
        try:
            return self.auth_service.update_image_s3(user)
        except Exception as error:
            raise error
