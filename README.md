# Proceso para desplegarlo en local.

## 1. Crear un entorno virtual.

```bash
python3 -m venv venv
```

## 2. Activar el entorno virtual.

```bash
source venv/bin/activate
```

Para ejecutar este proyecto localmente, hay que crear el `.env` en el directorio base y configurar las variables de entorno.

## 3. Instalar el paquete de dependencias.

```bash
pip install -r requirements.txt
```

## 4. Migrar/crear base de datos.

Inicializa el directorio de migraciones de la base de datos.

```bash
flask db init
```

Actualiza la base de datos con la última migración.

```bash
flask db upgrade
```

## 5. Finalmente, ejecutar el servidor.

Una vez que la base de datos esté configurada, puedes iniciar el servidor Flask para comenzar a usar la aplicación..

```bash
flask run
```

Para acceder a esta aplicación, abre `http://localhost:5000`
