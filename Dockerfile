# Usa una imagen oficial de Python 3.9
FROM python:3.9

# Evita que Python guarde archivos de caché `.pyc`
ENV PYTHONUNBUFFERED 1

# Actualiza paquetes del sistema, instala dependencias y limpia caché
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos antes de instalar dependencias para aprovechar la caché de Docker
COPY ./requirements.txt /requirements.txt

# Instala las dependencias de Python en una sola capa para optimización
RUN pip install --upgrade pip && pip install -r /requirements.txt

# Crea y usa el directorio `/app`
RUN mkdir -p /app
WORKDIR /app
COPY ./app /app


# Crea el usuario y grupo antes de asignar permisos
RUN addgroup --system django-group && \
    adduser --system --no-create-home --ingroup django-group django-user

# Expone el puerto 8000
EXPOSE 8000

# Cambia al usuario django-user
USER django-user


# Cambia al usuario no root DESPUÉS de ejecutar collectstatic
USER django-user
# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]

