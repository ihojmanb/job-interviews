# Pelea de Personajes
En este documento encontrarás:
* las instrucciones de ejecución del código
* la lógica de las peleas
* highlights del código que hace cumplir con los requerimientos del problema 
  
# [Instrucciones de ejecución](#Instrucciones-de-ejecución)

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
```
pip3 install -r requirements.txt
```

### ejecutar `setup.py` en modo `develop`
```
python3 setup.py develop
```

###  editar `credentials_template.json`
Debes renombrar este archivo a `credentials.json` 
```
mv credentials_template.json credentials.json
```
y agregar el `access-token` que te entrega la SuperHero API. Debería verse así:
```
{
    "access-token": "1234567890"
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
# [Lógica de la pelea](lógica-de-la-pelea)
La Pelea se lleva a cabo en `client.py`. Como estrategia de diseño se determinó que sería los equipos, a traves de un mediador, los que pelearían. Así, los personajes le comunican el *damage* de sus ataques a sus respectivos equipos, y estos los notifican al mediador, quien se hará cargo de enviar el mensaje al otro equipo, y este de traspasárselo al personaje que está peleando.

La pelea siempre la parte el el mismo equipo por defecto, y se van alternando los golpes. Los ataques son elegidos al azar.

 Los personajes pelean por como están ordenados en la lista `team.members` de cada equipo. Como los equipos se armaron de manera aleatoria, en estricto rigor los personajes pelean en un orden aleatorio.


# [Highlights](highlights)
El modelo debe cumplir con los siguientes requisitos:
1. los equipos se crean de forma aleatoria
2. no puede haber personajes repetidos
3. Para cada personaje, por cada uno de sus *stats*, se le asigna una nueva variable aleatoria de stamina
4. Los equipos definen su `alignment` como igual al `alignment` de la mayoría de los miembros del equipo
5. A cada personaje se le aplica una bonificación/penalización, conocida como *Filliation Coefficient*.
6. Los personajes tienen tres ataques

En `client.py` se crean 2 equipos:
```python
    list_of_random_characters = superhero_api_consumer.get_random_list_of_characters(10)

...
    team1 = team_creator.build_team(
        team_name="Equipo 1", list_of_characters=list_of_random_characters[0:5]
    )
    team2 = team_creator.build_team(
        team_name="Equipo 2", list_of_characters=list_of_random_characters[5:]
    )   
...

```
El método `get_random_list_of_characters(10)` hace un llamado a la API de SuperHero pidiendo 10 personajes cuyos ids sean completamente distintos. Conociendo de antemano el total del personajes existentes, podemos crear una muestra de 10 ids únicos:
```python
    def get_list_of_ids(self, number_of_ids):
        list_of_ids = random.sample(range(1, self.total_number_of_characters), k=number_of_ids)
        return list_of_ids
```
Nos aseguramos del que los ids son únicos con el siguiente test en `test_superhero_api.py`:
```python
    # We need to secure that there are not going to be repeted characters
    def test_ids_are_unique(self, random_id_list):
        unique_ids = set(random_id_list)
        assert len(random_id_list) == len(unique_ids)  # there are no repetitions

```
Por ende, sabemos que los equipos se arman de forma aleatoria con personajes que no se repiten, satisfaciendo `1.` y `2.`.

Para satisfaer `4.` tenemos en  `characters.py` el siguiente trozo de código:
```python
    def set_stats(self, attributes):

        powerstats = attributes["powerstats"]
        for stat, power in powerstats.items():
            # Setting stats attributes as ints
            self.__setattr__(stat, int(power) if power != "null" else 0)
            # Setting actual stamina per stat
            stamina = self.get_stamina()
            self.__setattr__(f"AS_{stat}", stamina)

```
En el mismo archivo, satisfacemos `5.` con:
```python
    def set_filliation_coefficient(self, team_alignment):
        fc = self.calculate_filliation_coefficient(team_alignment)
        self.__setattr__("filliation_coefficient", fc)

...
    def calculate_filliation_coefficient(self, team_alignment):
        numerical_team_alignment = 1 if team_alignment == "good" else -1
        coefficient = 1 + random.randrange(10)
        if self.alignment == numerical_team_alignment:
            return coefficient
        else:
            return math.pow(coefficient, -1)

```
y satisfacemos `6.` con:
```python
    def set_attacks(self):
        self.set_mental_attack()
        self.set_strong_attack()
        self.set_fast_attack()

    def set_mental_attack(self):
        mental_attack_value = (
            (self.intelligence * 0.7)
            + (self.speed * 0.2)
            + (self.combat * 0.1) * self.filliation_coefficient
        )
        self.__setattr__("mental_attack", mental_attack_value)

    def set_strong_attack(self):
        strong_attack_value = (
            (self.strength * 0.6)
            + (self.power * 0.2)
            + (self.combat * 0.2) * self.filliation_coefficient
        )
        self.__setattr__("strong_attack", strong_attack_value)

    def set_fast_attack(self):
        fast_attack_value = (
            (self.speed * 0.55)
            + (self.durability * 0.25)
            + (self.strength * 0.2) * self.filliation_coefficient
        )
        self.__setattr__("fast_attack", fast_attack_value)

```

# [Qué se puede mejorar](qué-se-puede-mejorar)
El módulo `client.py` está tremendamente *hardcodeado* porque fue lo último que escribí. Falta hacer una reescritura de este módulo y su respectivo testeo.

Aumentar el *test coverage* en todos los módulos. Si bien existe harto test para los módulos más importantes, al momento de escribir `client.py` se extendieron módulos sin el testeo apropiado.

Hacer mejor uso de los patrones de diseño.

Tener un pipeline de ejecución del programa más pulido.