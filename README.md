# Plantilla de microservicio


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

#### Ejecutando peticiones
1. Las peticiones deben realizarse al host `http://localhost:8000`
