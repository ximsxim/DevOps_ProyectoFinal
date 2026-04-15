#!/bin/bash
set -e
LOG_FILE="/var/log/syslog"
HISTORIAL="/home/ubuntu/historial_limpieza.txt"
if [ -f "$LOG_FILE" ]; then
    sudo truncate -s 0 "$LOG_FILE"
    echo "Limpieza de logs realizada el: $(date)" >> "$HISTORIAL"
else
    echo "Archivo $LOG_FILE no encontrado. No se realizo limpieza." >> "$HISTORIAL"
fi