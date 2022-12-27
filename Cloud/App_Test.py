from flask import Flask
import json
from app import * 

def test_routes_alive():
    app = Flask(__name__)
    app.secret_key = b'dont tell anyone'
    Configure_route(app)
    client = app.test_client()

    url = '/'
    response = client.get(url)
    assert response.status_code == 200

    url = '/Appmanager'
    response = client.get(url)
    assert response.status_code == 200

    url = '/item'
    response = client.get(url)
    assert response.status_code == 200

    url = '/keys'
    response = client.get(url)
    assert response.status_code == 302

    url = '/upload-image'
    response = client.get(url)
    assert response.status_code == 200

def test_uploadimage_pass ():
    p = 0