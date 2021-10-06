# Pelea de Personajes
En este documento encontrarás:
* las instrucciones de ejecución del código
* highlights del código que hace cumplir con los requerimientos del problema 
## Instrucciones de ejecución

### Clonar branch `toku` del repo
Para clonar sólo la rama que contiene el desafío:
```
git clone -b toku https://github.com/ihojmanb/job-interviews.git

```
Una vez clonado entramos al directorio `assignment` que contiene todo el código que nos interesa:
```
cd job-interviews/toku/assignment/
```
###  Instalar dependencias
TODO

###  editar `credentials_template.json`
Debes renombrar este archivo a `credentials.json` 
```
mv credentials_template.json credentials.json
```
y agregar el `access-token` que te entrega la SuperHero API:
```
{
    "access-token": "Your access token goes here "
}
```
### ejecutar `client.py`
Para ejecutar el programa interactivo en la terminal:
```
python3 src/client/client.py
```
### ejecutar tests
Para ejecutar todos los tests:
```
pytest -q -s tests/
```


