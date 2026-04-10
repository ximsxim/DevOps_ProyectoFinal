#!/bin/bash
# Este script vacía el archivo de logs del sistema para ahorrar espacio
sudo truncate -s 0 /var/log/syslog
echo "Limpieza de logs realizada el: $(date)" >> /home/ubuntu/historial_limpieza.txt