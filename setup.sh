#!/bin/bash
echo "Actualizando el sistema..."
sudo apt update -y
echo "Instalando git, vim, docker y python3..."
sudo apt install -y git vim docker.io python3 python3-pip
echo "¡Instalación completada a la perfección!"