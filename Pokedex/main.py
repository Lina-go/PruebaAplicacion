###################################################################################################
# Imports Generales
###################################################################################################

from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
from database import Base, Pokemon, Sprite, Ability
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

        # Se accede a la BD de Pokemon
        session = Session()
        pokemon = session.query(Pokemon).filter_by(id=id_pokemon).first()
        session.close()

        if not pokemon:
            return render_template('search_by_id_general.html', pokemon_json=None, error='Pokémon no encontrado')

        # Se muestra unicamente la info. solicitada
        detalles = {
            'nombre': pokemon.nombre,
            'recurso': pokemon.recurso,
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

        # Acceder a la BD de Pokemon por nombre
        session = Session()
        pokemon = session.query(Pokemon).filter_by(nombre=nombre_pokemon.lower()).first()
        session.close()

        if not pokemon:
            return render_template('search_by_nombre_general.html', detalles=None, error='Pokémon no encontrado')

        # obtener el recurso del pokemon
        url = pokemon.recurso

        # Construir dict de acuerdo a los solicitado
        detalles = {
            'nombre': pokemon.nombre,
            'recurso': url,
        }
        return render_template('search_by_nombre_general.html', detalles=detalles)

    return redirect(url_for('search_by_nombre_general'))



###################################################################################################
# Búsqueda Específica
###################################################################################################

# Ruta General
@app.route('/search_by_id_especifico', methods=['GET']) 
def search_by_id_especifico():
    return render_template('search_by_id_especifico.html')

@app.route('/buscar_id_especifico', methods=['POST', 'GET'])
def buscar_pokemon_por_id_especifico():
    if request.method == 'POST':
        id_pokemon = request.form.get('id')

        # Se accede por Id a la BD
        session = Session()
        pokemon = session.query(Pokemon).filter_by(id=id_pokemon).first()

        if not pokemon:
            session.close()
            return render_template('search_by_id_especifico.html', detalles=None, error='Pokémon no encontrado')

        # Busca las habilidades del pokemon por id
        abilities = session.query(Ability).filter_by(pokemon_id=id_pokemon).all()
        abilities_names = [ability.name for ability in abilities]

        # Busca los sprites del pokemon por id
        sprites = session.query(Sprite).filter_by(pokemon_id=id_pokemon).all()
        sprite_urls = [sprite.url for sprite in sprites]

        # Cierra la sesión
        session.close()

        # Prepara los datos para renderizar el template
        detalles = {
            'nombre': pokemon.nombre,
            'habilidades': abilities_names,
            'numero_pokedex': pokemon.id,
            'sprites': sprite_urls,
            'tipo': pokemon.tipo
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

        # Accede y busca el pokemon por nombre
        session = Session()
        pokemon = session.query(Pokemon).filter_by(nombre=nombre_pokemon.lower()).first()

        if not pokemon:
            session.close()
            return render_template('search_by_nombre_especifico.html', detalles=None, error='Pokémon no encontrado')

        # Busca las habiliades del pokemon por id
        abilities = session.query(Ability).filter_by(pokemon_id=pokemon.id).all()
        abilities_names = [ability.name for ability in abilities]

        # Busca los sprites del pokemon por id
        sprites = session.query(Sprite).filter_by(pokemon_id=pokemon.id).all()
        sprite_urls = [sprite.url for sprite in sprites]

        # Cierra la sesión
        session.close()

        # Prepara el template
        detalles = {
            'nombre': pokemon.nombre,
            'habilidades': abilities_names,
            'numero_pokedex': pokemon.id,
            'sprites': sprite_urls,
            'tipo': pokemon.tipo
        }
        return render_template('search_by_nombre_especifico.html', detalles=detalles)

    return redirect(url_for('search_by_nombre_especifico'))

###################################################################################################
# UPDATE
###################################################################################################
@app.route('/update_pokemon/<int:pokemon_id>/<new_name>/<new_recurso>', methods=['GET'])
def update_pokemon(pokemon_id, new_name, new_recurso):
    session = Session()
    pokemon = session.query(Pokemon).filter_by(id=pokemon_id).first()

    if pokemon:
        
        pokemon.nombre = new_name
        pokemon.recurso = new_recurso

        # Commit los cambios a la bd
        session.commit()
        session.close()

        return f'Updated Pokémon ID {pokemon_id} with new name: {new_name} and new type: {new_recurso}'
    else:
        session.close()
        return f'Pokémon with ID {pokemon_id} not found in the database.'
if __name__ == '__main__':
    app.run(debug=True)
