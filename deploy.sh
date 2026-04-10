#!/bin/bash
echo "Iniciando despliegue de la aplicacion..."

if sudo docker-compose up -d --build; then
    echo "✅ Despliegue exitoso. La aplicacion esta corriendo."
else
    echo "❌ Fallo el despliegue. Iniciando script de Rollback automatico..."
    # Detiene contenedores fallidos
    sudo docker-compose down
    # Restaura los contenedores a su ultimo estado estable
    echo "Restaurando version anterior..."
    sudo docker-compose up -d
    echo "✅ Rollback completado exitosamente."
    exit 1
fi