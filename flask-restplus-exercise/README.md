# Coding exercise

* a flask api app providing a GET endpoint
  * api
  * doc
  * unittest

## Set up

* `python3 -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`

## Run app

* `python app.py`

## Api doc/demo

* `http://localhost:5000/`

## Run tests

* `python test_app.py`


### Data
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
