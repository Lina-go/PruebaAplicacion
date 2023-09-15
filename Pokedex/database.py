##############################################  
# imports
##############################################

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests


##############################################
# Configuración de la base de datos
##############################################

DATABASE_URL = 'sqlite:///pokedex.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)  

Base = declarative_base()
##############################################
# Modelo Relacional de la base de datos
##############################################
class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    recurso = Column(String)
    tipo = Column(String)

class Sprite(Base):
    __tablename__ = 'sprites'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))

class Ability(Base):
    __tablename__ = 'abilities'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))

def init_db():
    Base.metadata.create_all(engine)

def fetch_and_insert_pokemon_data(pokemon_id):
    session = Session()  #Crea la sesión

    # Obtiene los datos del API
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()

        # Extrae los datos del API
        name = pokemon_data['name']
        type = ', '.join([type_data['type']['name'] for type_data in pokemon_data['types']])

        #  Inserta los datos en la base de datos
        pokemon = Pokemon(nombre=name, recurso=url, tipo=type)
        session.add(pokemon)
        session.commit()

        # Inserta sprites en la base de datos
        for sprite_url in pokemon_data['sprites']:
            sprite = Sprite(url=sprite_url, pokemon_id=pokemon.id)
            session.add(sprite)

        # Inserta habilidades en la base de datos
        for ability_data in pokemon_data['abilities']:
            ability_name = ability_data['ability']['name']
            ability = Ability(name=ability_name, pokemon_id=pokemon.id)
            session.add(ability)

        session.commit()
        print(f"Data for Pokémon {pokemon_id} inserted into the database.")
    else:
        print(f"Failed to fetch data for Pokémon {pokemon_id}.")

###############################################
# Inicialización de la base de datos
###############################################

if __name__ == '__main__':
    init_db()  
    start_id = 1  
    end_id = 20   
    for pokemon_id in range(start_id, end_id + 1):
        fetch_and_insert_pokemon_data(pokemon_id)
