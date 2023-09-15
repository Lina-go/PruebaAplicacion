###################################################################################################
# Imports Generales
###################################################################################################

from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
from database import Base, Pokemon
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

###################################################################################################
# Configuración de Flask Y Database
###################################################################################################

app = Flask(__name__)

DATABASE_URL = 'sqlite:///pokedex.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


###################################################################################################
# Ruta Principal
###################################################################################################

@app.route('/', methods=['GET'])
def search_options():
    return render_template('search_options.html')

# Ruta para la página principal
@app.route('/buscar', methods=['GET', 'POST'])
def choose_search_option():
    if request.method == 'POST':
        option = request.form.get('option')
        if option == 'id_general':
            print("Se oprimió ID general")
            return redirect(url_for('search_by_id_general')) 
        elif option == 'id_especifico':
            print("Se oprimió ID especifico")  
            return redirect(url_for('search_by_id_especifico'))  
        elif option == 'nombre_general':
            print("Se oprimió Nombre general")
            return redirect(url_for('search_by_nombre_general'))
        elif option == 'nombre_especifico':
            print("Se oprimió Nombre especifico")
            return redirect(url_for('search_by_nombre_especifico'))


    return redirect(url_for('search_options'))

###################################################################################################
# Búsqueda General
###################################################################################################

"""                                BÚSQUEDA POR ID GENERAL                                      """

@app.route('/search_by_id_general', methods=['GET']) 
def search_by_id_general():
    return render_template('search_by_id_general.html')


@app.route('/buscar_id_general', methods=['POST', 'GET'])
def buscar_pokemon_por_id_general():
    if request.method == 'POST':
        id_pokemon = request.form.get('id')

        # Fetch Pokémon data from the PokeAPI based on the ID
        url = f"https://pokeapi.co/api/v2/pokemon/{id_pokemon}/"
        response = requests.get(url)

        if response.status_code != 200:
            return render_template('search_by_id_general.html', pokemon_json=None, error='Pokémon no encontrado')

        pokemon_data = response.json()
        print(pokemon_data.keys())
        # Process and format the data as required before rendering the template
        detalles = {
            'nombre': pokemon_data['name'],
            'recurso': url,
        }
        return render_template('search_by_id_general.html', detalles=detalles)

    return redirect(url_for('search_by_id_general'))

"""                                BÚSQUEDA POR NOMBRE GENERAL                                      """
@app.route('/search_by_nombre_general', methods=['GET'])  
def search_by_nombre_general():
    return render_template('search_by_nombre_general.html')

@app.route('/buscar_nombre_general', methods=['POST', 'GET'])
def buscar_pokemon_por_nombre_general():
    if request.method == 'POST':
        nombre_pokemon = request.form.get('nombre')

        # Construct the URL for the Pokémon based on the name
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}/"

        # Fetch Pokémon data from the PokeAPI based on the name
        response = requests.get(url)

        if response.status_code != 200:
            return render_template('search_by_nombre_general.html', detalles=None, error='Pokémon no encontrado')

        pokemon_data = response.json()
        print(pokemon_data.keys())

        # Extract only the required fields for general search
        detalles = {
            'nombre': pokemon_data['name'],
            'recurso': url,
        }
        return render_template('search_by_nombre_general.html', detalles=detalles)

    return redirect(url_for('search_by_nombre_general'))  # Corrected route name


###################################################################################################
# Búsqueda Específica
###################################################################################################

# Route to render the search by ID page for general search
@app.route('/search_by_id_especifico', methods=['GET'])  # Corrected route name
def search_by_id_especifico():
    return render_template('search_by_id_especifico.html')

@app.route('/buscar_id_especifico', methods=['POST', 'GET'])
def buscar_pokemon_por_id_especifico():
    if request.method == 'POST':
        id_pokemon = request.form.get('id')

        # Fetch Pokémon data from the PokeAPI based on the ID
        url = f"https://pokeapi.co/api/v2/pokemon/{id_pokemon}"
        response = requests.get(url)

        if response.status_code != 200:
            return render_template('search_by_id_especifico.html', pokemon_json=None, error='Pokémon no encontrado')

        pokemon_data = response.json()

        # Process and format the data as required before rendering the template
        detalles = {
            'nombre': pokemon_data['name'],
            'habilidades': [habilidad['ability']['name'] for habilidad in pokemon_data['abilities']],
            'numero_pokedex': pokemon_data['id'],
            'sprites': pokemon_data['sprites'],
            'tipo': ', '.join([tipo['type']['name'] for tipo in pokemon_data['types']])
        }
        return render_template('search_by_id_especifico.html', detalles=detalles)

    return redirect(url_for('search_by_id_especifico'))

@app.route('/search_by_nombre_especifico', methods=['GET'])  # Corrected route name
def search_by_nombre_especifico():
    return render_template('search_by_nombre_especifico.html')

@app.route('/buscar_nombre_especifico', methods=['POST', 'GET'])
def buscar_pokemon_por_nombre_especifico():
    if request.method == 'POST':
        nombre_pokemon = request.form.get('nombre')

        # Construct the URL for the Pokémon based on the name
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}/"

        # Fetch Pokémon data from the PokeAPI based on the name
        response = requests.get(url)

        if response.status_code != 200:
            return render_template('search_by_nombre_especifico.html', detalles=None, error='Pokémon no encontrado')

        pokemon_data = response.json()
        print(pokemon_data.keys())

        # Extract only the required fields for general search
        detalles = {
            'nombre': pokemon_data['name'],
            'habilidades': [habilidad['ability']['name'] for habilidad in pokemon_data['abilities']],
            'numero_pokedex': pokemon_data['id'],
            'sprites': pokemon_data['sprites'],
            'tipo': ', '.join([tipo['type']['name'] for tipo in pokemon_data['types']])
        }
        return render_template('search_by_nombre_especifico.html', detalles=detalles)

    return redirect(url_for('search_by_nombre_especifico'))

if __name__ == '__main__':
    app.run(debug=True)
