# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Union
import base64
from datetime import datetime
import boto3
from app.schemas.auth.auth_schemas import UserLoginSchema, UserSignupSchema
from app.config.aws_setting import AwsSettings
from app.schemas.auth.auth_schemas import (UserCognitoLoginSchema, UserCognitoNewPasswordSchema,
                                           UserCognitoSignupSchema, UserSchema,
                                           UserUpdateImageSchema, GetUserSchema)
from app.exceptions.auth_exceptions import (NotAuthorized, UserNotFound, InvalidCode,
                                            InvalidSession, UserAlreadyExists, InvalidPassword,
                                            ServerError)


class AuthService:
    def __init__(self) -> None:
        self.boto3_client = boto3.client("cognito-idp")
        self.aws_settings = AwsSettings()

    def signin(self, user: UserLoginSchema) -> Union[UserCognitoLoginSchema,
                                                     UserCognitoNewPasswordSchema]:
        try:
            response = self.boto3_client.initiate_auth(
                ClientId=self.aws_settings.app_client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    "USERNAME": user.email,
                    "PASSWORD": user.password
                }
            )
            print(response)
            if "ChallengeName" in response and response["ChallengeName"] == "NEW_PASSWORD_REQUIRED":
                return UserCognitoNewPasswordSchema.from_dict(response)
            user = self.get_user(
                response["AuthenticationResult"]["AccessToken"])
            return UserCognitoLoginSchema.from_dict(response, user)
        except self.boto3_client.exceptions.NotAuthorizedException as error:
            print(error)
            raise NotAuthorized() from error
        except self.boto3_client.exceptions.UserNotFoundException as error:
            raise UserNotFound() from error

    def signup(self, user: UserSignupSchema) -> UserCognitoSignupSchema:
        try:
            if user.image != "":
                url_image = self.save_image_to_s3(user.image)
            else:
                url_image = "https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png"
            response = self.boto3_client.admin_create_user(
                UserPoolId=self.aws_settings.user_pool_id,
                Username=user.email,
                UserAttributes=[
                    {"Name": "email", "Value": user.email},
                    {"Name": "given_name", "Value": user.first_name},
                    {"Name": "family_name", "Value": user.last_name},
                    {"Name": "picture", "Value": url_image},
                    {"Name": "custom:role", "Value": user.role},
                    {"Name": "email_verified", "Value": "true"},
                ],
                DesiredDeliveryMediums=["EMAIL"],
            )
            return UserCognitoSignupSchema.from_dict(response)
        except self.boto3_client.exceptions.UsernameExistsException as error:
            raise UserAlreadyExists() from error
        except Exception as error:
            raise error

    def first_signin(self, user: UserLoginSchema) -> UserCognitoLoginSchema:
        try:
            response = self.boto3_client.admin_respond_to_auth_challenge(
                UserPoolId=self.aws_settings.user_pool_id,
                ClientId=self.aws_settings.app_client_id,
                ChallengeName="NEW_PASSWORD_REQUIRED",
                ChallengeResponses={
                    "USERNAME": user.email,
                    "NEW_PASSWORD": user.password,
                },
                Session=user.session,
            )
            user = self.get_user(
                response["AuthenticationResult"]["AccessToken"])
            return UserCognitoLoginSchema.from_dict(response, user)
        except self.boto3_client.exceptions.CodeMismatchException as error:
            raise InvalidCode() from error
        except self.boto3_client.exceptions.ExpiredCodeException as error:
            raise InvalidSession() from error
        except self.boto3_client.exceptions.NotAuthorizedException as error:
            raise InvalidSession() from error
        except self.boto3_client.exceptions.InvalidPasswordException as error:
            raise InvalidPassword() from error

    def signout(self, accesstoken: str) -> dict:
        try:
            response = self.boto3_client.global_sign_out(
                AccessToken=accesstoken
            )
            return response
        except self.boto3_client.exceptions.NotAuthorizedException as error:
            print(error)
            raise NotAuthorized() from error
        except self.boto3_client.exceptions.UserNotFoundException as error:
            raise UserNotFound() from error

    def get_user(self, accesstoken: str) -> UserSchema:
        try:
            response = self.boto3_client.get_user(
                AccessToken=accesstoken
            )
            return UserSchema.from_dict(response)
        except self.boto3_client.exceptions.NotAuthorizedException as error:
            print(error)
            raise NotAuthorized() from error
        except self.boto3_client.exceptions.UserNotFoundException as error:
            raise UserNotFound() from error
        except Exception as error:
            raise error

    def save_image_to_s3(self, image: str) -> str:
        try:
            image_b64 = base64.b64decode(image)
            filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            s3_client = boto3.client("s3")
            s3_client.put_object(
                Body=image_b64,
                Bucket=self.aws_settings.bucket_name,
                Key=filename,
                ACL='public-read'
            )
            url = f"https://{self.aws_settings.bucket_name}.s3.amazonaws.com/{filename}"
            return url
        except Exception as error:
            print(error)
            raise error

    def update_image_s3(self, user: UserUpdateImageSchema):
        try:
            response = self.boto3_client.admin_get_user(
                UserPoolId=self.aws_settings.user_pool_id,
                Username=user.email
            )

            url_old_image = response["UserAttributes"][6]["Value"]
            name_old_image = url_old_image.split("/")[-1]
            s3_client = boto3.client("s3")
            # update image
            image_b64 = base64.b64decode(user.image)
            s3_client.put_object(
                Body=image_b64,
                Bucket=self.aws_settings.bucket_name,
                Key=name_old_image,
                ACL='public-read'
            )
            return f"https://{self.aws_settings.bucket_name}.s3.amazonaws.com/{name_old_image}"
        except self.boto3_client.exceptions.UserNotFoundException as error:
            raise UserNotFound() from error
        except Exception as error:
            print(error)
            raise ServerError() from error

    def get_all_users(self):
        response = self.boto3_client.list_users(
            UserPoolId=self.aws_settings.user_pool_id,
            AttributesToGet=[
                'email',
                'given_name',
                'family_name',
                'picture',
                'custom:role'
            ],
        )
        print(response)
        users = []
        for user in response["Users"]:
            users.append(GetUserSchema.from_dict(user))
        return users
