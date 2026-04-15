#!/bin/bash
set -e
echo "Iniciando despliegue de la aplicacion..."
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "Error: docker-compose no instalado."
    exit 1
fi
if $DOCKER_COMPOSE up -d --build; then
    echo "Despliegue exitoso."
else
    echo "Fallo el despliegue. Iniciando rollback..."
    $DOCKER_COMPOSE down
    echo "Restaurando version anterior..."
    $DOCKER_COMPOSE up -d
    echo "Rollback completado."
    exit 1
fi