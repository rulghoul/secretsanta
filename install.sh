#!/bin/bash

# Variables Eventos
export EVENTOS_SQL_ENGINE="django.db.backends.mysql"
export EVENTOS_SQL_DATABASE="eventos"
export EVENTOS_SQL_USER="eventos"
export EVENTOS_SQL_PASSWORD="eventosdjango"
export EVENTOS_SQL_HOST="127.0.0.1"
export EVENTOS_SQL_PORT="3306"

#Crear Usuario y asignar permisos
groupadd --system webapps
useradd --system --gid webapps --home "/var/www/python/Fiesta" eventos

chown -R eventos:webapps /var/www/python/Fiesta
chmod +x gunicorn_eventos.bash

#Crear Base de datos

# Datos de conexión a la base de datos
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD=""
echo "Ingrese la contraseña para la conexión a la base de datos:"

read -s DB_PASSWORD

# Comandos SQL para crear bases de datos y usuarios
SQL1="CREATE DATABASE IF NOT EXISTS $EVENTOS_SQL_DATABASE;"
SQL1+="GRANT ALL PRIVILEGES ON $EVENTOS_SQL_DATABASE.* TO '$EVENTOS_SQL_USER'@'$DB_HOST' IDENTIFIED BY '$EVENTOS_SQL_PASSWORD';"

echo "Bases de datos y usuarios creados correctamente."

mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e "$SQL1" || exit 1


#Crear entorno virtual y descargar las librerias
python3 -m venv virtual
source virtual/bin/activate

# Exportar las variables de entorno al entorno virtual
export EVENTOS_SQL_ENGINE
export EVENTOS_SQL_DATABASE
export EVENTOS_SQL_USER
export EVENTOS_SQL_PASSWORD
export EVENTOS_SQL_HOST
export EVENTOS_SQL_PORT

echo "Instalar librerias"
pip3 install -r requirements.txt
cd fiestas

echo "Recreando tablas..."

python3 manage.py migrate

echo "Generando archivos estaticos..."

python3 manage.py collectstatic
python3 manage.py createsuperuser

echo "Repoblando tablas..."

python3 manage.py loaddata inicio.json
python3 manage.py loaddata catalogos02.json

echo "Generando usuario principal"

python3 manage.py createsuperuser
cd ..
deactivate

echo "Se termino de configurar el sistema con python"
mkdir logs
mkdir run

#Instalar supervisor

echo "Se crea el servicio Eventos con supervisor..."

cp eventos.conf /etc/supervisor/conf.d/eventos.conf
#Actualizar supervisor
supervisorctl reread
supervisorctl update
supervisorctl status

echo "Se termino de crear elservicio eventos"

echo "Se copia la configuracion de eventos"
#Configuracion de Nginx
cp nginx /etc/nginx/sites-available/eventos
#Activar sitio Nginx
ln -s /etc/nginx/sites-available/eventos /etc/nginx/sites-enabled/eventos
service nginx restart


