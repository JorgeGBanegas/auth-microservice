# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from app.services.auth_service import AuthService

def get_auth_service():
    return AuthService()
