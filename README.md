<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/drorganvidez/flask_base/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/drorganvidez/flask_base/actions/workflows/tests.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/drorganvidez/flask_base/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/drorganvidez/flask_base/actions/workflows/commits.yml)</a>
  
</div>

# flask_boilerplate

Base project to work with the Python Flask framework in an easy way.

## Set `.env` file in root with:

Create an `.env` file in the root of the project with this information.

```
cp .env.docker.example .env
```

## Deploy in develop

To deploy the software under development environment, run:

```
docker compose -f docker/docker-compose.dev.yml up -d 
```

This will apply the migrations to the database and run the Flask application. Open `http://localhost` to play with your fantastic app!

### Migrations

However, if during development there are new changes in the model, run inside the `web_app_container` container:

```
flask db migrate
flask db upgrade
```

### Tests

To run unit test, please enter inside `web_app_container` container:

```
rosemary test
```

## Deploy in production (Docker Compose)

```
docker compose -f docker/docker-compose.prod.yml up -d 
```
