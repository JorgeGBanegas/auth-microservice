# pylint: disable=missing-module-docstring
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from v1.api import app as v1_app

load_dotenv()

app = FastAPI(
    title="MicroServicio de autenticación",
    description="API para el MicroServicio de autenticación",
    version="1.0.0",
)
fronted_domain = os.getenv("DOMAIN_FRONT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[fronted_domain],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# pylint: disable=missing-function-docstring
@app.get("/api")
async def root():
    return {
        "message": "Bienvenido a la API de autenticación",
        "version": "1.0.0",
        "author": "Jorge Gustavo Banegas Melgar",
        "email": "jorge.g.banegas@gmail.com",
        "github": "https://github.com/JorgeGBanegas"
    }


app.mount("/api/v1", v1_app)

if __name__ == "__main__":
    import uvicorn
    print("Running on port 8001")
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)
