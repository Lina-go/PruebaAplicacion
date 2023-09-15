###############################################################################################
# IMPORTS
###############################################################################################

import os
import sys
import pytest

###############################################################################################
# SETTING DIR
###############################################################################################

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_search_by_id_general(client):
    response = client.get('/search_by_id_general')
    assert response.status_code == 200

def test_search_by_nombre_general(client):
    response = client.get('/search_by_nombre_general')
    assert response.status_code == 200

def test_search_by_id_especifico(client):
    response = client.get('/search_by_id_especifico')
    assert response.status_code == 200

def test_search_by_nombre_especifo(client):
    response = client.get('/search_by_nombre_especifico')
    assert response.status_code == 200

