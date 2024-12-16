<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/test.yml)</a>
  <a href="">[![Snyk Vulnerability Scan](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/snyk.yml/badge.svg?branch=main)](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/snyk.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/commits.yml)</a>

</div>


# diplomas-innosoft-1

Este es el proyecto de la asignatura EGC para crear diplomas para los alumnos organizadores y participantes en las jornadas InnoSoft.

# Manual de Uso para el Despliegue de la Aplicación

# Despliegue en Local
## 1. Clonar el Repositorio
Clonar el repositorio por las claves SSH e inicializarlo en el IDE preferido.

## 2. Configuración de MariaDB

### 2.1 Iniciar el Servicio de MariaDB
```bash
sudo systemctl start mariadb
```

### 2.2 Asegurar la Instalación de MariaDB
Esto configurará la contraseña del usuario root.
```bash
sudo mysql_secure_installation
```

### 2.3 Acceder a MySQL como el Usuario Root
```bash
sudo mysql -u root -p
```

### 2.4 Crear las Bases de Datos Necesarias
```sql
CREATE DATABASE diplomasdb;
CREATE DATABASE diplomasdb_test;
```

### 2.5 Crear un Nuevo Usuario con Privilegios sobre las Bases de Datos
```sql
CREATE USER 'diplomasdb_user'@'localhost' IDENTIFIED BY 'diplomasdb_password';
GRANT ALL PRIVILEGES ON diplomasdb.* TO 'diplomasdb_user'@'localhost';
GRANT ALL PRIVILEGES ON diplomasdb_test.* TO 'diplomasdb_user'@'localhost';
```

### 2.6 Aplicar los Cambios y Salir de MySQL
```sql
FLUSH PRIVILEGES;
EXIT;
```

## 3. Crear y Activar el Entorno Virtual de Python

### 3.1 Crear el Entorno Virtual
```bash
python3.12 -m venv venv
```

### 3.2 Activar el Entorno Virtual
```bash
source venv/bin/activate
```

## 4. Instalar las Dependencias del Proyecto

### 4.1 Copiar el Archivo de Configuración de Ejemplo a .env
```bash
cp .env.local.example .env
```

### 4.2 Actualizar pip a la Última Versión
```bash
pip install --upgrade pip
```

### 4.3 Instalar las Dependencias del Archivo requirements.txt
```bash
pip install -r requirements.txt
```

### 4.4 Instalar el Proyecto en Modo Editable
```bash
pip install -e ./
```

## 5. Ejecutar las Migraciones de la Base de Datos

### 5.1 Aplicar las Migraciones a la Base de Datos
```bash
flask db upgrade
```

### 5.2 Crear Nuevas Migraciones si es Necesario
```bash
flask db migrate
```

## 6. Iniciar el Proyecto
```bash
flask run
```
El servidor se ejecutará en [http://localhost:5000/](http://localhost:5000/)

## 7. Para ejecutar las pruebas:
### Pruebas unitarias y de intregración
```bash
rosemary test
```
### Pruebas de selenium
 - Cambiar el archivo init.py de la carpeta app de "development" a "testing."
- Ejecutar los siguientes comandos:
  - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`

- Iniciamos la aplicación:
`flask run`
- Ejecutamos los tests módulo a módulo: 
  `pytest <ruta del archivo te test_selenium.py>`

### Pruebas de locust 
 - Cambiar el archivo init.py de la carpeta app de "testing" a "development."
- Ejecutar los siguientes comandos:
  - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`

- Iniciamos la aplicación:
`flask run`
- Ejecutamos los tests módulo a módulo: 
  `rosemary locust <modulo>`


### Para ver la cobertura
```bash
rosemary coverage
```

## 8. Iniciar Sesión en el Proyecto

### 8.1 Credenciales de Acceso:
- **Correo electrónico:** user1@example.com
- **Contraseña:** password
## 9. Otros Detalles Importantes
- Verificar que las bases de datos `diplomasdb` y `diplomasdb_test` estén configuradas correctamente.
- Asegurarse de que estás utilizando la versión correcta de Python (Python 3.12).
- Si encuentras problemas con las dependencias, revisa el archivo `requirements.txt` y actualiza las librerías.
- Se recomienda que **siempre que se cambie un .env** se realicen los siguientes comandos:
  - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`


# Despligue en Máquina Virtual

## 1. Pasos anteriores
- Una vez seguidos los pasos 2, 3, 4, y 5 anteriormente mencionados en "Despliegue en Local", ejecutar lo siguiente:
```bash
cp .env.vagrant.example .env
```
Y ejecutar los siguientes comandos:
   - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`


## 2. Instalar Vagrant, VirtualBox y Ansible sobre Ubuntu 22.04 (Jammy Jellyfish):
Actualizamos la lista de paquetes:
```bash
sudo apt update
```
Instalar vagrant, ansible y virtualbox
```bash
sudo apt install vagrant ansible virtualbox
```
Si el paquete vagrant no está disponible tendrás que añadir manualmente el repo oficial y la clave GPG:
```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install vagrant ansible virtualbox
```
## 3. Instalación del programa Virtual Box
- **VirtualBox**: [Descargar aquí](https://www.virtualbox.org/wiki/Downloads)

## 4. Desactivar el modo "Secure Boot" en la BIOS

Para desactivar el modo "Secure Boot", sigue estos pasos:

1. Reinicia tu equipo y accede a la BIOS/UEFI (generalmente presionando teclas como **F2**, **Del**, o **Esc** al arrancar).
2. Busca la opción **Secure Boot** en el menú de configuración de seguridad o arranque.
3. Cámbiala a **Disabled** o **Off**.
4. Guarda los cambios y reinicia el equipo.

## 5. Eliminar las siguientes carpetas:
```bash
rm -r uploads
rm -r rosemary.egg-info
rm app.log*
```

## 6. Desplazarse a la carpeta vagrant
```bash
cd vagrant/
```
## 7. Levantar la máquina virtual por primera vez
```bash
vagrant up
```
El servidor se ejecutará en [http://localhost:5000/](http://localhost:5000/)
## 8. Conectar a la máquina virtual
```bash
vagrant ssh
```
## 9. Apagar la máquina virtual
```bash
vagrant halt
```
## 10. Para volver a ejecutar los scripts de provisión o se quiere volver a iniciar la máquina tras haber sido apagada:
 - **Si la máquina virtual está apagada:** ```vagrant up --provision```
 - **Si la máquina virtual necesita reiniciarse:** ```vagrant reload --provision```


## 11. Iniciar Sesión en el Proyecto

### 11.1 Credenciales de Acceso:
- **Correo electrónico:** user1@example.com
- **Contraseña:** password

## 12. Destruimos la máquina virtual
Vemos las máquinas virtuales que tenemos funcionando en nuestro sistema:
```bash
vagrant global-status
```
Destruimos la máquina virtual:
```bash
vagrant destroy <uuid>
```

**Notas:**
- Si hay errores y no reconoce algún comando **es recomendable eliminar el entorno virtual** y **volver a instalarlo** con los pasos del **punto 3 y 4** de "Despligue en Local" (con el **.env** correspondiente que se quiera usar).
- Si la máquina virtual se apaga, para volverla a iniciar correctamente se deben usar los comandos descritos en el **punto 7.6**.

## 13. Otros Detalles Importantes
- Verificar que las bases de datos `diplomasdb` y `diplomasdb_test` estén configuradas correctamente.
- Asegurarse de que estás utilizando la versión correcta de Python (Python 3.12).
- Si encuentras problemas con las dependencias, revisa el archivo `requirements.txt` y actualiza las librerías.
- Se recomienda que **siempre que se cambie un .env** se realicen los siguientes comandos:
  - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`

# Despliegue en Docker

## 1. Pasos anteriores
- Una vez seguidos los pasos 2, 3, 4, y 5 anteriormente mencionados en "Despliegue en Local", ejecutar lo siguiente:
```bash
cp .env.docker.example .env
```
Y ejecutar los siguientes comandos:
   - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`


## 2. Instalar Docker Compose

- El primer paso es descargar la última versión de Docker Compose. No obstante, las últimas versiones de Docker ya incluyen Docker Compose. Antes de intentar realizar una instalación de Docker Compose, lanza el siguiente comando:

```bash
docker compose version
```

- Si te funciona, puedes saltarte el paso de descargar e instalar Docker Compose. Si no, puedes descargar Docker Compose usando el siguiente comando, pero asegúrate de verificar la última versión en la página de lanzamientos de Docker Compose:

```bash
mkdir -p ~/.docker/cli-plugins/

LATEST_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

sudo curl -SL "https://github.com/docker/compose/releases/download/${LATEST_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o ~/.docker/cli-plugins/docker-compose
```

- Aplicar Permisos Ejecutables: asegúrate de que el archivo de Docker Compose tenga permisos ejecutables:

```bash
chmod +x ~/.docker/cli-plugins/docker-compose
```

- Verificar la instalación de Docker Compose: para confirmar que Docker Compose se ha instalado correctamente, ejecuta:

```bash
docker compose --version
```


## 3. Parar el proceso de Mariadb en el puerto 3306
Debido a que MariaDb por defecto se inicia en el puerto 3306 (el cual necesita docker), debemos parar el proceso de la aplicación, para ello ejecutamos:
```bash
sudo systemctl stop mariadb
```
Verificamos que se ha parado con el comando: `sudo lsof -i :3306`
## 4. Construir y levantar una imagen de Docker

```bash
docker-compose -f docker/docker-compose.yml up --build -d
```
El servidor se ejecutará en [http://localhost:5000/](http://localhost:5000/)

Si queremos parar Docker:
```bash
docker-compose -f docker/docker-compose.yml down
```


## 5. Iniciar Sesión en el Proyecto

### 5.1 Credenciales de Acceso:
- **Correo electrónico:** user1@example.com
- **Contraseña:** password

## 6. Matamos el contenedor de Docker
```bash
sh scripts /clean_docker.sh
```
## 7. Iniciamos de nuevo MariaDb
```bash
sudo systemctl start mariadb
```


**Notas:**
- Si hay errores y no reconoce algún comando **es recomendable eliminar el entorno virtual** y **volver a instalarlo** con los pasos del **punto 3 y 4** de "Despligue en Local" (con el **.env** correspondiente que se quiera usar).



## 8. Otros Detalles Importantes
- Verificar que las bases de datos `diplomasdb` y `diplomasdb_test` estén configuradas correctamente.
- Asegurarse de que estás utilizando la versión correcta de Python (Python 3.12).
- Si encuentras problemas con las dependencias, revisa el archivo `requirements.txt` y actualiza las librerías.
- Se recomienda que **siempre que se cambie un .env** se realicen los siguientes comandos:
  - `flask db downgrade`
  - `flask db upgrade`
  - `flask db migrate`

