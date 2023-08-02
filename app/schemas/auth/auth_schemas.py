# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
from pydantic import BaseModel, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSignupSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    image: str
    role: str

class UserSchema(UserSignupSchema):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data["UserAttributes"][2]["Value"],
            last_name=data["UserAttributes"][3]["Value"],
            role=data["UserAttributes"][4]["Value"],
            email=data["UserAttributes"][5]["Value"],
            image=data["UserAttributes"][6]["Value"],
        )

class UserCognitoNewPasswordGetSchema(UserLoginSchema):
    session: str

class UserCognitoSignupSchema(UserSignupSchema):
    status: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data["User"]["Attributes"][2]["Value"],
            last_name=data["User"]["Attributes"][3]["Value"],
            role=data["User"]["Attributes"][4]["Value"],
            email=data["User"]["Attributes"][5]["Value"],
            image=data["User"]["Attributes"][6]["Value"],
            status=data["User"]["UserStatus"],
        )

class UserCognitoLoginSchema(BaseModel):
    access_token: str
    expires_in: int
    id_token: str
    refresh_token: str
    token_type: str
    user: UserSchema
    @classmethod
    def from_dict(cls, data: dict, user: UserSchema):
        return cls(
            access_token=data["AuthenticationResult"]["AccessToken"],
            expires_in=data["AuthenticationResult"]["ExpiresIn"],
            id_token=data["AuthenticationResult"]["IdToken"],
            refresh_token=data["AuthenticationResult"]["RefreshToken"],
            token_type=data["AuthenticationResult"]["TokenType"],
            user=user,
        )

class UserCognitoNewPasswordSchema(BaseModel):
    challenge_name: str
    session: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            challenge_name=data["ChallengeName"],
            session=data["Session"],
        )

class UserUpdateImageSchema(BaseModel):
    image: str
    email: EmailStr
