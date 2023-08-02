# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
from fastapi import HTTPException

class NotAuthorized(HTTPException):
    def __init__(self):
        detail = {
            "message": "Email o contraseña incorrecta",
            "error": "No autorizado"  
        }
        super().__init__(status_code=401, detail=detail)

class UserNotFound(HTTPException):
    def __init__(self):
        detail = {
            "message": "Usuario no encontrado",
            "error": "No autorizado"  
        }
        super().__init__(status_code=404, detail=detail)

class InvalidCode(HTTPException):
    def __init__(self):
        detail = {
            "message": "El codigo ingresado es invalido",
            "error": "Codigo invalido"  
        }
        super().__init__(status_code=400, detail=detail)

class InvalidSession(HTTPException):
    def __init__(self):
        detail = {
            "message": "La sesion ha expirado",
            "error": "Sesion invalida"  
        }
        super().__init__(status_code=400, detail=detail)

class UserAlreadyExists(HTTPException):
    def __init__(self):
        detail = {
            "message": "El usuario ya existe",
            "error": "Usuario ya existe"  
        }
        super().__init__(status_code=409, detail=detail)

class TokenNotFound(HTTPException):
    def __init__(self):
        detail = {
            "message": "Nececitas un token valido para realizar esta accion",
            "error": "Token no encontrado"  
        }
        super().__init__(status_code=404, detail=detail)

class TokenNotValid(HTTPException):
    def __init__(self):
        detail = {
            "message": "El token no es valido",
            "error": "Token no valido"  
        }
        super().__init__(status_code=400, detail=detail)

class InvalidPassword(HTTPException):
    def __init__(self):
        detail = {
            "message": "La contraseña debe tener al menos 8 caracteres, \
                una letra mayuscula, una letra minuscula, un numero y un caracter especial",
            "error": "Contraseña invalida"  
        }
        super().__init__(status_code=400, detail=detail)

class ServerError(HTTPException):
    def __init__(self):
        detail = {
            "message": "Ha ocurrido un error en el servidor",
            "error": "Error en el servidor"  
        }
        super().__init__(status_code=500, detail=detail)
