# Microservicio de empresas clientes

## Cómo ejecutar

1. Clonar el repositorio
2. Ejecutar `docker-compose build` en la raíz del proyecto
3. Ejecutar `docker-compose up` en la raíz del proyecto

También es posible ejecutar el proyecto sin hacer uso de contenedores, para esto:
1. Clonar el repositorio
2. Ejecutar `pip3 install -r requirements.txt`
3. Ejecutar `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
  
## Cómo usar
1. El componente se encontrará en el puerto 8000 de la máquina host

### Cómo poblar las bases de datos
Este proyecto hace uso de una base de datos PostgreSQL y el ORM SQLAlchemy. Adicionalmente, se hace uso de la herramienta alembic para la creación y ejecución de seeders de la base de datos.

Para hacer uso de la alembic es necesario modificar la propiedad `sqlalchemy.url` encontrada en el archivo `alembic.ini` que se encuentra en la raíz del proyecto para que apunte a la base de datos deseada.

A continuación se listan los comandos para crear y ejecutar una nueva migración:

1. Para crear una migración: `alembic revision -m "Set up Customer table"`
2. Para ejecutar las migraciones pendientes: `alembic upgrade head`, o `alembic upgrade <version_id>` para la migración deseada

#### Ejecutando peticiones
1. Las peticiones deben realizarse al host `http://localhost:8000`
