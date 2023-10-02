# Proyecto de testeo Backend en Flask de Is2-2023
# Proyecto de testeo realizado por:
- Elizabeth Bravo Campos
- Gustavo Gonzalez Gutierrez
- Esteban Suazo Montalba

## Dependencias
Las dependencias necesarias para ejecutar el proyecto de Flask son las siguientes:
- flask, flask-cors, flask-migrate, flask-bcrypt, flaks-sqlAlchemy
Pueden ser instalados de la siguiente forma en un entorno virutal o sobre una terminal normal:

```
pip install flask flask-cors flask-migrate flask-bcrypt flask-sqlAlchemy
```
## Ejecutando el proyecto
- Para ejecutar el proyecto se debe estar ubicado en la ruta:
  /testing_project1/is2_backend/lib/api
- y ejecutar el siguiente comando:
```
flask --app dbAPI run
```
## Ejecutando los test
- Los test fueron implementados con pytest, por lo que debe ser instalado de antemano.
- Para ser ejecutados se debe posicionar en la carpeta is2_backend con el servidor de Flask corriendo en otra terminal
y ejecutando:

```
pytest 
```
