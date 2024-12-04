# pitrivals-backend
Backend para la aplicación web Pit Rivals

# Dependencias
- Git
- Python 3.11 [Enlace de descargas](https://www.python.org/downloads/)

# Configuración del proyecto
1. Instalar repositorio
` git clone https://github.com/Pit-Rivals/pitrivals-backend.git`

2. Entrar en el directorio del repositorio
`cd pitrivals-backend`

3. Descargar virtualenv (si no lo tienes instalado)
`pip install virtualenv`

4. Crear entorno virtual
`virtualenv .venv`

5. Abrir el entorno virtual creado
`source .venv/Scripts/activate`

6. Instalar dependencias
`pip install -r requirements.txt`

# Ejecutar servidor local
Establecer entorno mediante la variable de entorno `FLASK_ENV`: `export FLASK_ENV=<dev o prod>`
Desde el directorio `src/flaskapp`, ejecutar el comando `flask run --debug`

Podrás acceder al servidor del navegador a través de la URL  http://127.0.0.1:5000

CTRL+C para cerrarlo.

# Antes de subir cambios
Si hay cambios en los paquetes de Python utilizados, actualizar el requirements:
`python -m pip freeze > requirements.txt`