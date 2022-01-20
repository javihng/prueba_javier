from flask import Flask, render_template, request, jsonify, abort
from flask_lazyviews import LazyViews
import requests


app = Flask(__name__)
views = LazyViews(app)

@app.route('/')
def inicio():
    return render_template('index.html', title="Star Wars")


@app.route('/peliculas')
def peliculas():
    response = requests.get('https://swapi.dev/api/films')
    lista_peliculas = response.json()['results']

    return render_template('peliculas.html', title="Peliculas Star Wars", peliculas=lista_peliculas)


@app.route('/personajes')
def personajes():

    return render_template('personajes.html')


@app.route('/traer_personaje')
def traer_personajes_pelicula():
    id_personaje = request.args.get('id_personaje')

    response_personajes = requests.get(f'https://swapi.dev/api/people/{id_personaje}')

    if not response_personajes.ok:
        abort(404, description="Personaje no existe, intente con un ID del 1 al 83")

    info_personaje = response_personajes.json()

    info_basica_personaje = {'id': id_personaje,
                             'nombre': info_personaje['name'],
                             'altura': info_personaje['height'],
                             'color_cabello': info_personaje['hair_color'],
                             'anio_nacimiento': info_personaje['birth_year']}


    return jsonify(result=info_basica_personaje)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


app.run(host='0.0.0.0')