# Usa Python 3.11
FROM python:3.11-slim

# Establece directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expón el puerto que usará FastAPI/Uvicorn
EXPOSE 8000

# Comando para iniciar el bot
CMD ["python", "apiclima.py"]