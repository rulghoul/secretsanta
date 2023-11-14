#!/bin/bash

#Crear Usuario y asignar permisos
groupadd --system webapps
useradd --system --gid webapps --home "/var/www/python/secretsanta" santa

chown -R santa:webapps /var/www/python/secretsanta
chmod +x gunicorn_santa.bash

#Crear entorno virtual y descargar las librerias
python3 -m venv virtual
source virtual/bin/activate

echo "Instalar librerias"
pip3 install -r requirements.txt


echo "Se termino de configurar el sistema con python"
mkdir logs
mkdir run

#Instalar supervisor

echo "Se crea el servicio Eventos con supervisor..."

cp santa.conf /etc/supervisor/conf.d/santa.conf
#Actualizar supervisor
supervisorctl reread
supervisorctl update
supervisorctl status

echo "Se termino de crear elservicio Intercambio"

echo "Se copia la configuracion de Intercambio"
#Configuracion de Nginx
cp nginx /etc/nginx/sites-available/santa
#Activar sitio Nginx
ln -s /etc/nginx/sites-available/santa /etc/nginx/sites-enabled/santa
service nginx restart


