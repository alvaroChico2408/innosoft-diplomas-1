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
