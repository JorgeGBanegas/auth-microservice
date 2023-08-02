# pylint: disable=missing-module-docstring
from fastapi import FastAPI
from v1.endpoints.auth_routes import router as auth

app = FastAPI()

app.include_router(auth, prefix="/auth", tags=["Authentication"])
