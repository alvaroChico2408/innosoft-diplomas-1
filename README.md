<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/test.yml)</a>
  <a href="">[![Snyk Vulnerability Scan](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/snyk.yml/badge.svg?branch=main)](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/snyk.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/alvaroChico2408/innosoft-diplomas-1/actions/workflows/commits.yml)</a>7

</div>


# diplomas-innosoft-1

Este es el proyecto de la asignatura EGC para crear diplomas para los alumnos organizadores y participantes en las jornadas InnoSoft.

# Manual de Uso para el Despliegue de la Aplicación en Local

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
El servidor se ejecutará en [http://127.0.0.1:5000/](http://127.0.0.1:5000/)



## 7. Iniciar el Proyecto en la Máquina Virtual
### 7.1 Copiar el Archivo de Configuración (Vagrant) de Ejemplo a .env
```bash
cp .env.vagrant.example .env
```
### 7.2 Desplazarse a la carpeta vagrant
```bash
cd vagrant/
```
### 7.3 Levantar la máquina virtual por primera vez
```bash
vagrant up
```
El servidor se ejecutará en [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
### 7.4 Conectar a la máquina virtual
```bash
vagrant ssh
```
### 7.5 Apagar la máquina virtual
```bash
vagrant halt
```
### 7.6 Para volver a ejecutar los scripts de provisión o se quiere volver a iniciar la máquina tras haber sido apagada:
 - **Si la máquina virtual está apagada:** ```vagrant up --provision```
 - **Si la máquina virtual necesita reiniciarse:** ```vagrant reload --provision```

**Notas:**
- Para volver a desplegar el proyecto en **localhost** (usando `flask run`) o en **Docker**, se recomienda **eliminar el entorno virtual** y volver a crearlo siguiendo los pasos descritos en el **punto 3**.
- Si la máquina virtual se apaga, para volverla a iniciar correctamente se deben usar los comandos descritos en el **punto 7.6**.
- Se recomienda eliminar los datos de la base de datos si se quiere volver a arrancar en local siguiendo los siguientes comandos:

    - Nos conectamos a MariaDB: `sudo mysql -u root -p`
    - Eliminamos las bases de datos de diplomasdb y diplomasdb_test:
    `DROP diplomasdb;` y `DROP diplomasdb_test;`.
    - Volvemos a realizar las migraciones con el .env que se quiera usar: `flask db upgrade` y `flask db migrate`.




## 8. Iniciar Sesión en el Proyecto

### 8.1 Credenciales de Acceso:
- **Correo electrónico:** user1@example.com
- **Contraseña:** password
## 9. Otros Detalles Importantes
- Verificar que las bases de datos `diplomasdb` y `diplomasdb_test` estén configuradas correctamente.
- Asegurarse de que estás utilizando la versión correcta de Python (Python 3.12).
- Si encuentras problemas con las dependencias, revisa el archivo `requirements.txt` y actualiza las librerías.


# Manual de Uso para el Despliegue de la Aplicación en Docker

## 1. Pasos anteriores
- Una vez seguidos los pasos 2, 3, 4, y 5 anteriormente mencionados.

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

## 3. Construir y levantar una imagen de Docker

```bash
docker-compose -f docker/docker-compose.yml up --build -d
```

- (Para parar Docker)
```bash
docker-compose -f docker/docker-compose.yml down --build -d
```

## 4. Verificación en el Navegador

Una vez que el contenedor esté en ejecución, abre tu navegador y accede a [http://localhost:5000](http://localhost:5000). Si ves la aplicación funcionando, ¡felicidades! Has dockerizado exitosamente la aplicación Flask.
