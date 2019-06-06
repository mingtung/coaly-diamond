# Coding exercise: flask-restplus app, documentation, and unittest

Two options to set up and run the app, 1. with venv or 2. with docker

### 1. Set up and run with venv

* set up
  ```
  $ python3 -m venv env
  $ pip install -r requirements.txt
  $ cd flask-app
  ```
* run app: `python app.py`
* api doc/demo: `http://localhost:5000/`
* run tests: `python test.py`

### 2. Set up and run docker container

```
# cd to where the `docker-compose.yml` file is
$ docker-compose up --build
```

* check the url `http://0.0.0.0` or `http://localhost`

## Data

Demo data is from wikidata. It is currently dumped and stored as json. It's worth to checkout sparql query in the future.

```
# select all astronauts with name, image, birthdate, birthplace and coordinates of the birthplace

SELECT DISTINCT ?astronaut ?astronautLabel ?image ?birthdate ?birthplace ?birthplaceLabel ?countryLabel(year(xsd:dateTime(?birthdate)) as ?birthyear) WHERE {
?astronaut ?x1 wd:Q11631;
wdt:P18 ?image;
wdt:P569 ?birthdate;
wdt:P19 ?birthplace.

#?birthplace wdt:P625 ?coord;
?birthplace wdt:P17 ?country;
SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?birthplace)
```
