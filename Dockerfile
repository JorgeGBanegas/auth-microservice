# Usa la imagen base oficial de Python
FROM python:3.10

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto del código fuente al directorio de trabajo
COPY . .

# Expone el puerto en el que FastAPI está ejecutando
EXPOSE 8001

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
