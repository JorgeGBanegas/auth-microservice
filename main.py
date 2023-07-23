# pylint: disable=missing-module-docstring
from fastapi import FastAPI

app = FastAPI(
    title="MicroServicio de autenticación",
    description="API para el MicroServicio de autenticación",
    version="1.0.0",
)

# pylint: disable=missing-function-docstring
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de autenticación",
        "version": "1.0.0",
        "author": "Jorge Gustavo Banegas Melgar",
        "email": "jorge.g.banegas@gmail.com",
        "github": "https://github.com/JorgeGBanegas"
    }


if __name__ == "__main__":
    import uvicorn
    print("Running on port 8001")
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)
