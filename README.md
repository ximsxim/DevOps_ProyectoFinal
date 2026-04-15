# Proyecto Final DevOps

## Descripcion
Este proyecto implementa un flujo completo de DevOps utilizando automatizacion, contenedores Docker e integracion continua y despliegue continuo (CI/CD) con GitHub Actions. El objetivo es automatizar la construccion, pruebas y despliegue de una aplicacion web en un entorno Linux (AWS EC2).

## Tecnologias utilizadas
- Docker
- Docker Compose
- GitHub Actions
- AWS EC2
- AWS CloudFormation
- AWS S3
- Bash
- Python con Boto3

## Estructura del proyecto

DevOps_ProyectoFinal/
├── .github/workflows/pipeline.yml
├── aws_manager.py
├── buildspec.yml
├── clean_logs.sh
├── deploy.sh
├── docker-compose.yml
├── Dockerfile
├── infra.yaml
├── README.md
└── setup.sh


## Decisiones tecnicas
- **Multi-stage build en Dockerfile**: Se utiliza una primera etapa basada en Alpine para generar el contenido estatico y una segunda etapa con nginx:alpine para servir el archivo. Esto reduce el tamano final de la imagen y mejora la seguridad.
- **Healthchecks en contenedores**: Se configuro un healthcheck en el servicio app_web para que Docker supervise el estado de la aplicacion y pueda reiniciarla automaticamente si falla.
- **Rollback automatico en deploy.sh**: El script de despliegue intenta levantar los contenedores con docker-compose. Si falla, ejecuta un down y vuelve a levantar la version anterior, garantizando disponibilidad.
- **Validacion de limites en script Python**: El script aws_manager.py verifica que exista la llave SSH 'llaves-devops', comprueba que no se superen 5 instancias EC2 activas (limite por defecto de la cuenta) y espera a que la instancia alcance el estado 'running' antes de continuar.
- **Proteccion de rama main**: Se configuro una regla de proteccion en GitHub que requiere Pull Request con al menos una aprobacion y que todos los status checks del pipeline pasen exitosamente antes de permitir el merge.
- **Pipeline con pruebas reales**: El pipeline de GitHub Actions no solo construye las imagenes, sino que valida la sintaxis de scripts Bash y Python, verifica la plantilla CloudFormation con la CLI de AWS, y ejecuta una prueba funcional con curl para confirmar que la aplicacion responde correctamente antes de desplegar.

## Validaciones implementadas
- **Scripts Bash**: uso de `set -e` para detener la ejecucion ante cualquier error, y verificacion de existencia de archivos (por ejemplo, `/var/log/syslog` en clean_logs.sh).
- **Script Python**: verificacion de existencia de la llave SSH, control de cuotas de EC2, espera de estado 'running' mediante waiter, y manejo especifico de excepciones de cliente.
- **CI/CD**: validacion sintactica de todos los scripts, validacion de la plantilla CloudFormation, prueba de respuesta HTTP del contenedor antes del despliegue.

## Requisitos previos para ejecucion local
- Tener instalados Docker y Docker Compose.
- Tener configuradas las credenciales de AWS (opcional, solo para scripts que interactuan con AWS).

## Ejecucion local

```bash
docker-compose up -d --build

La aplicacion estara disponible en:
http://localhost:8080

Para detener los contenedores:

docker-compose down
Pipeline CI/CD (GitHub Actions)

El pipeline se define en .github/workflows/pipeline.yml y se activa automaticamente con cada push a la rama main. Las etapas son:

Checkout: clona el codigo del repositorio.
Validar sintaxis de scripts Bash: ejecuta bash -n sobre setup.sh, clean_logs.sh y deploy.sh.
Validar sintaxis de Python: compila aws_manager.py con python -m py_compile.
Validar plantilla CloudFormation: usa aws cloudformation validate-template para verificar infra.yaml.
Construir imagenes Docker: ejecuta docker-compose build para validar que no hay errores en los Dockerfiles.
Prueba funcional: levanta los contenedores, espera 5 segundos y hace una peticion curl a http://localhost:8080. Si la respuesta es exitosa, continua; si no, falla el pipeline.
Copiar archivos a EC2: mediante appleboy/scp-action, envia todos los archivos del proyecto (excepto .git) al directorio /home/ubuntu/proyecto_docker en la instancia EC2.
Ejecutar despliegue remoto: mediante appleboy/ssh-action, se conecta a la instancia, asigna permisos de ejecucion a deploy.sh y ejecuta el script.
Mejoras implementadas por retroalimentacion

Basado en la evaluacion del maestro, se agregaron las siguientes mejoras para aumentar la robustez y profundidad tecnica:

Verificacion de llave SSH y limite de instancias en el script Python.
Uso de set -e y validacion de existencia de archivos en scripts Bash.
Deteccion automatica del comando docker-compose (version nueva vs antigua) y rollback automatico en deploy.sh.
Pipeline con pruebas reales (sintaxis, CloudFormation, respuesta HTTP).
Healthchecks y politica de reinicio en los contenedores.
Documentacion tecnica detallada en este README.
Referencias
Repositorio: https://github.com/ximsxim/DevOps_ProyectoFinal
Presentacion: https://canva.link/y1e72imb6qv7v36
