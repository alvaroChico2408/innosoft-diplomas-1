# Modelo de Uso

## 1. Política de ramas

### 1.1. Rama `main`
**Descripción:** La rama `main` es la rama principal y contiene el código que está listo para producción. Solo se actualiza cuando el código ha sido completamente probado en `preproduction`.

**Acciones permitidas:**
- **Merge desde `preproduction`:** Solo se permite hacer merge de la rama `preproduction` una vez que todas las pruebas en preproducción han sido exitosas.
- **No se permite el desarrollo directo:** No se debe desarrollar ni hacer commits directamente en `main`. Todo cambio debe pasar por `preproduction`.

**Uso:** Desplegar el código desde `main` a producción.

### 1.2. Rama `preproduction`
**Descripción:** Rama donde se prueban las características antes de que se integren en `main`. Aquí se hacen pruebas de integración y de preproducción. Esta rama actúa como un entorno de "ensayo" antes de producción.

**Acciones permitidas:**
- **Merge desde ramas de features:** Las ramas de características o correcciones salen de `preproduction` y, una vez finalizadas, se integran de vuelta en `preproduction`.
- **Pruebas de preproducción:** Todo el código debe ser probado a fondo en esta rama antes de ser fusionado en `main`.

**Uso:** Integrar y probar características nuevas, correcciones de errores y cambios antes de enviarlos a producción.

### 1.3. Ramas de características (`feature/*`)
**Descripción:** Las ramas `feature/*` son ramas temporales creadas para desarrollar nuevas funcionalidades o corregir errores. Cada tarea o característica debe tener su propia rama.

**Convención de nombre:** Se sigue la convención `feature/nombre-de-la-característica`.

**Caso especial:** Va a existir siempre una rama llamada `feature/docs` que al final de cada entrega se va a subir a la rama preproduction. En esta rama va a estar la documentación básica del proyecto.

**Acciones permitidas:**
- **Desarrollo y commits:** Los desarrolladores pueden crear nuevas ramas a partir de `preproduction` para trabajar en una nueva característica. Todos los commits relacionados con esa característica se realizarán en esta rama.
- **Merge en `preproduction`:** Una vez que la característica ha sido completada y probada localmente, se debe hacer un pull request (PR) y realizar un merge de la rama `feature/*` en `preproduction`.

**Uso:** Desarrollar nuevas características o corregir errores.

### 1.4. Rama `hotfix/*` (si es necesario)
**Descripción:** Estas ramas se utilizan para hacer correcciones rápidas en producción. Si se descubre un error crítico en `main` que debe corregirse inmediatamente, se crea una rama `hotfix/*` a partir de `main`.

**Convención de nombre:** Se sigue la convención `hotfix/nombre-del-hotfix`.

**Acciones permitidas:**
- **Desarrollo rápido:** Se desarrolla una solución rápida para corregir un error crítico en producción.
- **Merge en `main` y `preproduction`:** Una vez resuelto el error, se fusiona la rama `hotfix/*` tanto en `main` como en `preproduction` para asegurar que el código en ambas ramas esté alineado.

**Uso:** Corregir rápidamente errores críticos en producción sin esperar al ciclo de desarrollo habitual.

## 2. Flujo de Trabajo General:

### 2.1. Crear una nueva feature:
1. Crear una nueva rama `feature/nueva-característica` a partir de `preproduction`.
2. Desarrollar la nueva característica en esta rama.
3. Hacer commits frecuentemente en esta rama.

### 2.2. Integración de una feature:
1. Una vez que se termina el desarrollo de la característica, hacer un pull request desde `feature/nueva-característica` hacia `preproduction`.
2. Revisar el código y hacer merge en `preproduction` si pasa todas las revisiones.

### 2.3. Pruebas en `preproduction`:
1. Realizar pruebas exhaustivas en la rama `preproduction`.
2. Si se encuentra un problema, crear una nueva rama de feature para corregirlo y fusionarlo en `preproduction`.

### 2.4. Deploy a producción:
1. Una vez que todo el código en `preproduction` ha pasado las pruebas, hacer un pull request desde `preproduction` hacia `main`.
2. Hacer merge en `main` y desplegar el código en producción.

### 2.5. Corregir un error crítico (`hotfix`):
1. Si hay un error crítico en producción, crear una rama `hotfix/*` desde `main`.
2. Corregir el error en la rama `hotfix/*`.
3. Hacer merge en `main` y en `preproduction` para asegurar que la corrección esté en ambas ramas.

## 3. Política de commits
Se harán commits atómicos, que permitan un historial de commits claro y legible. Cada commit deberá contener un cambio autocontenido. Cada commit irá precedido de uno de los siguientes tópicos:

- `feat`: Nueva funcionalidad para el usuario.
- `fix`: Corrección de bugs/errores.
- `docs`: Cambios en la documentación.
- `styles`: Formato, cambios en frontend.
- `refactor`: Refactorizar código sin cambiar funcionamiento.
- `test`: Tests para probar las funcionalidades.
- `chore`: Actualizar tareas.
- `config`: Editar fichero de configuración.

Seguido de una descripción, con la primera letra en mayúscula.

El límite de la descripción del commit será de 75 caracteres.

Un ejemplo de commit: 

`[feat] Adapted email sending functionality`

## 4. Política de registros en Clockify

Cuando registres tiempo en **Clockify**, cada entrada debe ser clara y precisa. Cada descripción de registro debe estar precedida por un prefijo que identifique el tipo de trabajo que se está realizando.

### Prefijos para el tipo de trabajo:

- **`work`**: Para el tiempo dedicado a la investigación de temas relacionado con el proyecto y/o tecnología.
- **`meet`**: Para el tiempo invertido en reuniones de equipo.
- **`docs`**: Para el tiempo dedicado a actualizar o crear documentación, tanto de código como funcional.
- **`task`**: Para tareas relacionadas con el código y la programación.

### Formato de registro de tiempo:

Al insertar un registro de tiempo en **Clockify**, utiliza este formato:

`[work] Resolved problems with initialization`



