import json
from urllib.parse import unquote
from collections import defaultdict

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, abort


flask_app = Flask(__name__)
app = Api(app=flask_app,
          version='1.0',
          title='Demo astronaut names grouped by their birthplace',
          description='Show astronauts queried by their birthplace (country)'
                      ' then grouped by birthplace (city)')
astronauts_namespace = app.namespace('astronauts',
                                     description='APIs for astronauts info')
place_parser = app.parser()
place_parser.add_argument(
    'country',
    type=str, required=True,
    help="the country that is astronauts birthplace in string for which spaces "
         "are replaced by '-', e.g. United-States-of-America, Russia, etc")


def group_astronauts_by_city(data):
    if not data:
        return {}

    result = defaultdict(list)
    for person in data:
        astronaut_name = person.get('astronautLabel')
        city_label = person.get('birthplaceLabel')
        result[city_label].append(astronaut_name)

    return result


def get_astronauts_by_country(country):
    # TODO check possible api (wikidata)

    country = ' '.join(unquote(country).replace(' ', '').split('-'))
    with open('astronaut-all.json') as f:
        data = json.load(f)
        result = [i for i in data if i.get('countryLabel') == country]

    return result


@astronauts_namespace.route('')
@app.doc(responses={200: 'OK', 400: 'Invalid Argument',
                    502: 'Bad Gateway'})
class Astronauts(Resource):
    @app.expect(place_parser)
    def get(self):
        try:
            country = request.args.get('country')
            if not country:
                abort(400)
            data = get_astronauts_by_country(country)
            if data == 'api error':
                abort(502, custom='external api error')

            grouped_data = group_astronauts_by_city(data)
            return jsonify(grouped_data)

        except ValueError:
            abort(400, custom='author is invalid')


if __name__ == '__main__':
    flask_app.run(debug=True)
