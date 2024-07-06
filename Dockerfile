# Usar la imagen base de Alpine Linux
FROM python:3.10-alpine

# Instalar dependencias del sistema
RUN apk update && apk add --no-cache build-base libffi-dev openssl-dev

# Crear y activar un entorno virtual
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Definir el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de tu aplicación
COPY src/ /app/src/

# Exponer el puerto que usará Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "src/app.py"]
