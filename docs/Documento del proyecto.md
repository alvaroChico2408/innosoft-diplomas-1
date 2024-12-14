# Documento del proyecto - Proyecto innosoft-diplomas-1

## Indicadores del proyecto

Miembro del equipo  | Horas | Commits | LoC | Test | Issues | Tareas |
------------- | ------------- | ------------- | ------------- | ------------- | ------------- |  ------------- | 
[Aragón Sánchez, Alejandro](https://github.com/alearasan) | 36:34:43 (27:08:43, 04:40:00, 01:46:00, 03:00:00) | 33 | 1190 | 16 | 8 | Caso de uso de manejo de diplomas, caso de uso de creación de plantillas, documentación y labor primordial en el testing.
[Chico Castellano, Álvaro](https://github.com/alvaroChico2408) | 41:35:00 (15:45:00, 21:45:00, 00:10:00, 03:55:00) | 76 | 1877 | 7 | 6 | Creación y adaptación del primer proyecto base, migración de funcionalidad al nuevo y definitivo proyecto base, configuración de CI, despliegue en Render y testing.
[Guillén Fernandez, David](https://github.com/davguifer) | 53:30:04 (26:30:38, 17:17:35, 01:34:39, 08:07:12) | 47 | 1945 | 7 | 9 | Adaptar la funcionalidad del email en el primer proyecto base, creación y validación de diplomas a partir de un excel, migración de funcionalidad al nuevo y definitivo proyecto base, gestión del perfil, despliegue en máquinas virtuales, documentación y testing.
[Jiménez Osuna, Álvaro](https://github.com/Alvar0j) | 39:24:24 (08:25:08, 23:43:05, 02:26:38, 04:49:33) | 62 | 1740 | 7 | 9 | Configuración de envío de correos con los diplomas, configuración y creación de scripts para la CI, despliegue en Docker, documentación y testing.
[Linares Barrera, Jaime](https://github.com/Jaime-Linares) | 56:53:16 (29:20:17, 08:08:39, 12:50:22, 06:33:38) | 65 | 2858 | 10 | 17 | Generación y validación de diplomas a partir de un excel y una plantilla determinada, caso de uso de manejo de diplomas, caso de uso de envío de diplomas, ayuda en el caso de uso de creación de plantillas, correcciones en la migración de la funcionalidad entre proyectos, ayuda en la creación de scripts para la CI, documentación y testing.
[López Osuna, Ángela](https://github.com/angelalop03) | 19:29:46 (13:32:10, 00:00:00, 03:35:20, 02:22:16) | 22 | 1854 | 47 | 4 | Diseño de la interfaz del sistema (apariencia e interacción con el usuario), documentación y labor primordial en el testing.
**TOTAL** | 246:27:13 (120:41:56, 75:34:19, 22:22:59, 28:47:59)  | 305 | 11464 | 90 | 37 | Generador y edición de diplomas para los alumnos

La tabla contiene la información de cada miembro del proyecto y el total de la siguiente forma: 
  * Horas: número de horas empleadas en el proyecto en el siguiente formato `horas totales (horas en task, horas es work, horas en docs, horas en meetings)`. Si quiere conocer a que se refiere cada una le invito a ver el documento [Modelo de Uso.md](https://github.com/alvaroChico2408/innosoft-diplomas-1/blob/main/docs/Modelo%20de%20Uso.md).
  * Commits: número de commits hechos.
  * LoC (líneas de código): líneas de código producidas (las que se producen al incluir código de terceros no están incluidas).
  * Test: número de test realizados.
  * Issues: número de issues gestionadas.
  * Tareas: tareas en las que ha participado.

_Nota: Para ver la justificación del número de horas le invitamos a ver la carpeta `docs/clockify-reports`, para verificar el número de commits y líneas de código puede ver el siguiente enlace [insights](https://github.com/alvaroChico2408/innosoft-diplomas-1/graphs/contributors), para verificar el número de test puede comprobar los commits que llevan la etiqueta [test] y por último para el reparto de issues y tareas puede fijarse en el [tablero Kanban](https://github.com/users/alvaroChico2408/projects/4)._


## Resumen ejecutivo
En el presente trabajo se ha desarrollado un proyecto integral de generación de diplomas automatizados, con el objetivo de optimizar el proceso de creación, administración y distribución de diplomas personalizados a partir de datos contenidos en archivos Excel. Este sistema ofrece una solución eficiente y escalable para InnoSoft.

El proyecto surge de la necesidad de automatizar el proceso manual de generación de diplomas, que a menudo resulta tedioso y propenso a errores. Con esta solución, se busca reducir los tiempos de generación y distribución de diplomas, eliminar errores humanos en el manejo de datos, proporcionar herramientas flexibles para la personalización de plantillas, e integrar funcionalidades de gestión y distribución en un entorno único y accesible.

El sistema desarrollado cuenta con una serie de funcionalidades principales. Primero, permite cargar datos desde un archivo Excel, seleccionar plantillas predefinidas y generar diplomas personalizados, almacenando los datos en una base de datos para su posterior gestión y consulta. Segundo, incluye una sección de gestión que permite visualizar, filtrar, eliminar y enviar diplomas, ofreciendo una vista detallada de cada alumno y diploma generado. Tercero, proporciona herramientas para la creación de plantillas personalizadas a partir de un archivo PDF y texto, incluyendo una opción de previsualización para verificar el diseño antes de su uso. Finalmente, incluye una gestión de perfil para que los usuarios puedan actualizar su información personal y preferencias dentro del sistema.

Para garantizar la calidad y la estabilidad del sistema, se implementaron diversas pruebas automatizadas. Las pruebas unitarias verifican el correcto funcionamiento de las unidades más pequeñas del código. Las pruebas de interfaz, realizadas con Selenium, evalúan la experiencia del usuario al interactuar con el sistema. Las pruebas de carga, realizadas con Locust, simulan el uso simultáneo por múltiples usuarios para evaluar el rendimiento del sistema. Las pruebas de integración aseguran que los diferentes módulos trabajen correctamente en conjunto.

Además, el proyecto incorpora un sistema de integración continua para mantener altos estándares de calidad. Entre las tareas automatizadas destacan la verificación de la estructura de los commits, la ejecución de pruebas, el análisis de calidad del código con Codacy, la verificación de vulnerabilidades con Snyk, el despliegue en Render y la generación y despliegue de imágenes Docker. El sistema ha sido desplegado en entornos como Render, Docker y máquinas virtuales, lo que garantiza su portabilidad y facilidad de configuración.

El sistema desarrollado aporta múltiples beneficios. Entre ellos, destaca la eficiencia, ya que reduce significativamente el tiempo necesario para generar y distribuir diplomas. También mejora la fiabilidad al eliminar errores humanos, ofrece flexibilidad gracias a sus herramientas personalizables, es escalable para manejar grandes volúmenes de datos y usuarios, y garantiza seguridad mediante medidas para proteger la integridad de los datos y el sistema.

En conclusión, este proyecto representa un avance significativo en la automatización de procesos relacionados con la emisión de diplomas. Su enfoque integral y las buenas prácticas de desarrollo implementadas lo convierten en una herramienta útil, segura y escalable para instituciones educativas y otras organizaciones.


## Descripción del sistema
El sistema desarrollado es una aplicación web construida con el framework Flask, diseñada para automatizar y gestionar el proceso de generación de diplomas personalizados a partir de datos estructurados en un archivo Excel. Su diseño modular y escalable permite a InnoSoft optimizar la emisión de diplomas, desde la configuración de plantillas hasta la distribución digital de los documentos.

### Descripción funcional del sistema
Desde un punto de vista funcional, el sistema aborda diversas etapas del proceso de generación y administración de diplomas:

* Carga y procesamiento de datos: El usuario puede cargar un archivo Excel que contiene información relevante de los estudiantes, como nombres, apellidos, uvus, correo, entre otros. Una vez cargado, el sistema valida los datos y los almacena en una base de datos, garantizando su integridad y consistencia.

* Selección y personalización de plantillas: Los usuarios pueden elegir entre plantillas predefinidas o crear sus propias plantillas a partir de un archivo PDF, agregando texto personalizado. Esta funcionalidad incluye una vista previa en tiempo real para asegurar que el diseño sea adecuado antes de generar los diplomas.

* Generación de diplomas: Utilizando los datos almacenados y la plantilla seleccionada, el sistema genera diplomas en formato PDF de manera automatizada. Cada diploma se asocia a un registro específico en la base de datos para su posterior consulta o modificación.

* Gestión de diplomas: En una interfaz intuitiva, los usuarios pueden visualizar todos los diplomas generados, filtrarlos según criterios específicos, eliminar los registros no deseados y enviar los documentos por correo electrónico a los destinatarios seleccionados.

* Gestión de usuarios: El sistema incluye una sección donde los usuarios pueden gestionar su perfil, actualizando información personal como nombre, correo electrónico y contraseña.

### Arquitectura técnica
Desde una perspectiva arquitectónica, el sistema sigue una estructura modular basada en Flask, con una clara separación entre la lógica de negocio, la capa de presentación y la capa de datos. A continuación, se describen sus componentes principales:

* Frontend: La interfaz de usuario está desarrollada utilizando HTML, CSS y JavaScript para garantizar una experiencia de usuario responsiva y amigable.

* Backend: Construido sobre Flask, el backend maneja la lógica de negocio y expone endpoints para la comunicación con el frontend. Flask fue seleccionado por su simplicidad y flexibilidad, permitiendo implementar rápidamente funcionalidades como la generación de diplomas y la gestión de usuarios.

* Base de datos: El sistema utiliza una base de datos relacional (MariaDB) para almacenar información de usuarios, plantillas, y diplomas. SQLAlchemy actúa como ORM (Object-Relational Mapping) para facilitar la interacción con la base de datos.

* Generación de PDF: El sistema utiliza las bibliotecas PyPDF2 y ReportLab para la generación de diplomas en formato PDF. La integración de estas herramientas permite un procesamiento eficiente y flexible. PyPDF2 se encarga de la manipulación de archivos PDF existentes, como la edición de textos o la combinación de documentos. Por su parte, ReportLab se utiliza para crear contenido gráfico y textual desde cero, proporcionando un alto grado de personalización en los diseños.

    El flujo de generación de diplomas comienza con la selección de una plantilla base en formato PDF. A partir de esta plantilla, PyPDF2 permite abrir y preparar el documento para su edición. Luego, ReportLab genera una capa personalizada que incluye el texto y los elementos gráficos correspondientes a los datos del estudiante, como su nombre, curso y fecha. Esta capa se superpone sobre la plantilla utilizando las funcionalidades de PyPDF2 para producir un diploma finalizado.

* Correo electrónico: La funcionalidad de envío de diplomas utiliza el protocolo SMTP, con configuraciones para servidores de correo comunes como Gmail o servicios personalizados.

* Gestor de tareas: Para garantizar que las operaciones pesadas, como la generación masiva de diplomas o su envío por correo, no afecten el rendimiento del sistema, se ha implementado un gestor de tareas basado en Redis.

* Seguridad: Se han implementado medidas de seguridad como autenticación de usuarios mediante tokens, cifrado de contraseñas y validación estricta de datos para prevenir ataques.

### Relación entre componentes
La comunicación entre componentes está claramente definida para garantizar la coherencia del sistema. El frontend interactúa con el backend mediante API REST, enviando y recibiendo datos en formato JSON. El backend, a su vez, interactúa con la base de datos para almacenar y recuperar información.

### Desarrollo del proyecto
Durante el desarrollo del proyecto, se implementaron diversas funcionalidades, entre las que destacan:

* Diseño y creación de plantillas personalizables: Se agregó la capacidad de subir archivos PDF y editarlos para convertirlos en plantillas de diplomas.

* Previsualización en tiempo real: Se incorporó una funcionalidad para que los usuarios puedan verificar cómo se verán los diplomas antes de generarlos.

* Gestión avanzada de envío de correos: Se desarrolló un sistema para el envío selectivo de diplomas con seguimiento del estado de los envíos.

* Mejoras en la seguridad: Se implementaron controles adicionales para proteger la información sensible de los usuarios y garantizar la integridad del sistema.

* Automatización de pruebas y despliegues: Se incorporó un flujo de integración continua para verificar la calidad del código y facilitar el despliegue en múltiples entornos.

### Conclusión
El sistema desarrollado representa una solución robusta y eficiente para la generación automatizada de diplomas, integrando funcionalidades clave que abarcan desde la personalización hasta la distribución. Gracias a su diseño modular y su arquitectura escalable, está preparado para satisfacer las necesidades de diversas organizaciones y adaptarse a futuros requerimientos.


## Visión global del proceso de desarrollo (1.500 palabras aproximadamente)
El proceso de desarrollo del sistema de generación de diplomas automatizados se ha llevado a cabo de manera estructurada y orientada a la calidad. La metodología implementada combina buenas prácticas de gestión de proyectos, desarrollo ágil y herramientas modernas de integración continua, permitiendo un flujo de trabajo eficiente desde la conceptualización de las tareas hasta la implementación en producción.

### Etapas del proceso de desarrollo
#### 1. Creación y gestión de tareas
El ciclo de desarrollo comienza con la identificación de una necesidad o mejora. Esta se documenta en forma de issue en una plataforma de gestión de proyectos como GitHub. La issue incluye una descripción detallada de la tarea, los objetivos que se desean alcanzar y las dependencias o limitaciones relevantes. Además, se asigna un responsable para su ejecución y se define un criterio de aceptación claro.

#### 2. Desarrollo de la tarea
Una vez evaluada y aprobada la issue, comienza la etapa de desarrollo. El programador clona el repositorio correspondiente y crea una rama específica para la tarea, asegurando que los cambios realizados estén aislados del código principal. Durante esta fase, se emplean las herraminetas necesarias. Este proceso incluye la escritura de código modular y mantenible, con comentarios claros que faciliten futuras revisiones o ampliaciones.

#### 3. Pruebas
Terminada la implementación, se ejecutan pruebas para validar la funcionalidad. Estas incluyen:
* Pruebas unitarias: Verifican que las funciones individuales del nuevo código se comporten según lo esperado. Estas pruebas se implementan utilizando pytest.
* Pruebas de interfaz: Utilizando Selenium, se prueba la interacción del usuario con la nueva funcionalidad. Estas pruebas verifican que los elementos visuales respondan correctamente a las acciones del usuario.
* Pruebas de carga: Con Locust, se asegura que el sistema pueda manejar múltiples usuarios interactuando simultáneamente con la funcionalidad. Esto permite identificar posibles cuellos de botella o problemas de rendimiento.
* Pruebas de integración: Evalúan que el nuevo componente funcione correctamente junto con los módulos existentes, asegurando una comunicación fluida y sin errores entre componentes.

Cualquier fallo detectado en esta etapa se documenta y se corrige antes de continuar. Las pruebas son un paso fundamental para garantizar que los cambios no introduzcan errores en el sistema.

#### 4. Integración continua y revisión
Cuando las pruebas son satisfactorias, la rama con los cambios se sube al repositorio y se crea un pull request. En este punto, el sistema de integración continua ejecuta una serie de tareas automatizadas:
* Ejecución de las pruebas unitarias y de integración.
* Análisis de calidad del código con Codacy, que detecta problemas de estilo, complejidad y vulnerabilidades.
* Verificación de vulnerabilidades mediante Snyk, asegurando que las dependencias utilizadas en el proyecto sean seguras y estén actualizadas.
* Comprobación que la estrcutura de los commits sigue los estándares propuestos.

Si todos los pasos son exitosos, el pull request se revisa manualmente por otro miembro del equipo. Este proceso asegura que los cambios sean consistentes con los estándares del proyecto y que no se introduzcan errores inadvertidos.

#### 5. Despliegue en producción
El código actualizado se despliega en el entorno de producción utilizando Docker, Render o máquinas virtuales. Durante esta etapa, se realizan pruebas adicionales para garantizar que la funcionalidad implementada opere correctamente en el entorno real. El despliegue también incluye la configuración de registros y monitoreo para detectar posibles problemas en tiempo real.

El uso de contenedores Docker asegura que el entorno de producción sea consistente con el entorno de desarrollo, minimizando los riesgos de incompatibilidades. Render, como plataforma de despliegue, ofrece una solución fácil de escalar y administrar, mientras que las máquinas virtuales permiten configuraciones más personalizadas si es necesario.

#### 6. Cierre de la tarea
Finalmente, si la funcionalidad cumple con los criterios de aceptación definidos en la issue, esta se cierra, y el cambio se considera completo. Se documenta la mejora en el historial del proyecto para futuras referencias. Este paso también incluye la comunicación con el equipo o los usuarios para informar sobre las nuevas funcionalidades o cambios realizados.

### Conclusión
El enfoque estructurado y basado en herramientas modernas garantiza que cada cambio realizado en el sistema sea evaluado, implementado y desplegado con un alto nivel de calidad. Este proceso no solo optimiza el desarrollo, sino que también asegura que el sistema se mantenga estable y funcional a lo largo del tiempo. La combinación de metodologías de desarrollo ágil, integración continua y buenas prácticas de gestión permite un flujo de trabajo eficiente y adaptable a las necesidades del proyecto.


## Entorno de desarrollo
El entorno de desarrollo utilizado para el proyecto ha sido homogéneo para todos los integrantes del equipo, asegurando consistencia en la configuración y facilitando la colaboración. Esto ha permitido que los resultados sean replicables y que los desarrolladores puedan trabajar sin problemas de compatibilidad.

### Herramientas principales y versiones
* Sistema Operativo: Todos los miembros del equipo han utilizado distribuciones de Linux (Ubuntu 22.04 LTS), lo cual proporcionó un entorno estable y compatible con las herramientas necesarias para el desarrollo.
* Python: La versión utilizada fue Python 3.12, seleccionada por su compatibilidad con las bibliotecas y frameworks empleados en el proyecto.
* Framework Flask: Flask ha sido el framework principal para el desarrollo de la aplicación web, elegido por su flexibilidad y facilidad de uso.
* Gestor de paquetes: Se utilizó pip para la instalación de dependencias.
* Base de datos: Durante el desarrollo local se utilizó MariaDB, configurada con bases de datos separadas para la aplicación principal y para pruebas.
* Versionado de código: Git ha sido la herramienta principal para el control de versiones, con un repositorio centralizado en GitHub.
* Virtualización: Se usó Docker para la contenedorización de la aplicación y para garantizar la consistencia entre los entornos de desarrollo, pruebas y producción.
* Editor de texto/IDE: Los desarrolladores trabajaron principalmente con Visual Studio Code, aprovechando su extensibilidad y soporte para Python.
* Herramientas de integración continua: GitHub Actions para automatizar pruebas, despliegues y verificaciones de calidad.

### Instalación del sistema en local
A continuación, se detallan los pasos necesarios para configurar el sistema y ejecutarlo en un entorno local.

#### 1. Clonar el Repositorio
Clonar el repositorio por las claves SSH e inicializarlo en el IDE preferido:

        $ git clone git@github.com:usuario/proyecto-diplomas.git
        $ cd proyecto-diplomas

#### 2. Configuración de MariaDB
Iniciar el Servicio de MariaDB:

        $ sudo systemctl start mariadb

Asegurar la Instalación de MariaDB y configurar la contraseña del usuario root:

        $ sudo mysql_secure_installation

Acceder a MySQL como el Usuario Root:

        $ sudo mysql -u root -p

Crear las Bases de Datos Necesarias:

        CREATE DATABASE diplomasdb;
        CREATE DATABASE diplomasdb_test;

Crear un Nuevo Usuario con Privilegios sobre las Bases de Datos:

        CREATE USER 'diplomasdb_user'@'localhost' IDENTIFIED BY 'diplomasdb_password';
        GRANT ALL PRIVILEGES ON diplomasdb.* TO 'diplomasdb_user'@'localhost';
        GRANT ALL PRIVILEGES ON diplomasdb_test.* TO 'diplomasdb_user'@'localhost';
        FLUSH PRIVILEGES;
        EXIT;

#### 3. Crear y Activar el Entorno Virtual de Python
Crear el Entorno Virtual:

        $ python3.12 -m venv venv

Activar el Entorno Virtual:

        $ source venv/bin/activate

#### 4. Instalar las Dependencias del Proyecto
Copiar el Archivo de Configuración de Ejemplo a .env:

        $ cp .env.local.example .env

Actualizar pip a la última versión:

        $ pip install --upgrade pip

Instalar las Dependencias del Archivo requirements.txt:

        $ pip install -r requirements.txt

Instalar rosemay:

        $ pip install -e ./

#### 5. Ejecutar las Migraciones de la Base de Datos
Aplicar las Migraciones a la Base de Datos:

        $ flask db upgrade

Crear Nuevas Migraciones si es Necesario:

        $ flask db migrate

#### 6. Iniciar el Proyecto
Levantar el servidor de desarrollo:

        $ flask run

El servidor se ejecutará en [http://127.0.0.1:5000/](http://127.0.0.1:5000/).


## Ejercicio de propuesta de cambio
### Contexto del Cambio
El cambio propuesto consiste en modificar el título de la página principal para que todas las letras aparezcan en mayúscula (BIENVENIDO A DIPLOMAS INNOSOFT). Este cambio es sencillo pero ilustrativo de todo el proceso de gestión y evolución del proyecto.

### Pasos para Realizar el Cambio
#### 1. Crear la Issue
- Accede al tablero del proyecto en la plataforma de gestión de Kanban.
- Se crea una nueva issue con el siguiente detalle en TODO:
    - Título: Cambiar el título de la página de Home a mayúsculas.
    - Descripción: Modificar el título de la página principal del sistema para que todas las letras del texto sean mayúsculas.
    - Etiquetas: request of Change, low.
    - Se le asigna a una persona.

#### 2. Crear una Rama
- Cambia a la rama preproduccion:

        git checkout preproduccion
        git pull

- Crea una nueva rama para el cambio:

        git checkout -b feature/cambiar-titulo-home

- Mueve la issue en el tablero Kanban a "In Progress" para indicar que se ha iniciado el trabajo.

#### 3. Desarrollo del Cambio
- Realiza los cambios correspondientes para solucionar la propuesta de cambio.
- Si fuera necesario (que no es el caso), documenta brevemente el cambio en los comentarios del archivo para facilitar futuras referencias.

#### 4. Pruebas
- Inicia el servidor de desarrollo:
        
        flask run

- Abre el navegador en http://127.0.0.1:5000 y verifica que el título aparece en mayúsculas.
- Realiza las pruebas correspondientes para comprobar que todo funciona bien. En este caso habrá que hacer una prueba de Selenium.

#### 5. Subir al Repositorio
- Agrega y confirma los cambios:

        git add .
        git commit -m "[fix] title home view in capital letters"

- Sube los cambios al repositorio remoto:

    git push origin feature/cambiar-titulo-home

- Mueve la issue a "In Review" en el tablero Kanban para indicar que está lista para revisión.

#### 6. Crear Pull Request
- Crea una Pull Request desde la rama feature/cambiar-titulo-home hacia preproduccion.
- Agrega una descripción clara del cambio:
    - Descripción: Este Pull Request modifica el título de la página principal para que todas las letras aparezcan en mayúscula.
- Solicita revisión de un miembro del equipo.

#### 7. Revisar y Fusionar
- El revisor verifica que el cambio cumple con los criterios y aprueba la Pull Request.
- Verificar que se pasan los scripts de integración continua que realizarán pruebas automáticas para verificar que todo funciona correctamente, comprobará que los commits siguen los estándares, se lanzará un análisis de Codacy y se llevará a cabo un análisis con Snyk.

#### 8. Despliegue a Producción
- Cuando la integración continua confirme que todo está en orden en preproduccion, se seguirán los pasos 6 y 7 de nuevo pero ahora con destino a main (producción).
- Tras pasar todos los scripts de integración continua y despliegue continuo ya podemos comprobar tanto en el despliegue como en local que todo funciona correctamente.

#### 9. Cerrar la Tarea
- Una vez que todo esté comprobado, mueve la issue a "Done" en el tablero Kanban.
- Comunica al equipo que el cambio ha sido implementado exitosamente.

### Conclusión
Este ejercicio ilustra un ciclo completo de implementación de cambio en el sistema, desde la creación de una issue hasta su despliegue en producción. La integración continua garantiza que los cambios sean consistentes y de alta calidad, asegurando que el proyecto evolucione de manera ordenada y eficiente. El uso de revisiones y pruebas automáticas en cada etapa minimiza el riesgo de errores y mantiene la estabilidad del sistema.


## Conclusiones y trabajo futuro
### Conclusiones
El sistema desarrollado representa un avance significativo en la automatización de procesos relacionados con la generación de diplomas. A través de un diseño modular y el uso de herramientas modernas, se ha logrado optimizar el tiempo y reducir los errores en la creación y distribución de estos documentos. Además, el uso de entornos de desarrollo homogéneos y una metodología de integración continua han garantizado la calidad y estabilidad del sistema.

A pesar de los logros alcanzados, el desarrollo del sistema también ha permitido identificar áreas de mejora y posibles extensiones que podrían ser abordadas en futuros ciclos de desarrollo.

### Propuestas de Mejora

#### 1. Generación de Diplomas para Ponentes
Una mejora importante que se podría implementar en el futuro es la extensión del sistema para incluir la generación de diplomas destinados a los ponentes de eventos. Esta funcionalidad permitiría:
* Diseñar plantillas específicas para diplomas de reconocimiento a ponentes.
* Incorporar campos personalizados como el tema de la ponencia o la fecha del evento.
* Facilitar la gestión y distribución de estos diplomas a través del sistema existente.

#### 2. Mejora en la Integración con Servicios Externos
La integración con plataformas externas como Google Drive o Dropbox podría ofrecer a los usuarios la posibilidad de almacenar y compartir los diplomas de manera más eficiente. Además, la sincronización con herramientas de gestión de eventos podría automatizar aún más el flujo de trabajo.

#### 3. Funcionalidades Avanzadas de Reportes
Ampliar el sistema para incluir reportes estadísticos detallados sobre la generación y distribución de diplomas. Esto podría incluir:
* Informes por evento o por tipo de diploma generado.
* Gráficos interactivos que permitan analizar datos de forma visual.

#### 4. Mayor Personalización de Plantillas
Aunque el sistema actual permite diseñar plantillas personalizadas, se podría explorar la implementación de un editor visual más completo que ofrezca herramientas avanzadas para diseño, como arrastrar y soltar elementos, personalización de colores y tipografías.


