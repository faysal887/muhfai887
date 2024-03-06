import sys, os, json

visable_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(visable_dir)

# Now you can import 'solution' modules
from endpoint import app, load_model, predict_fasttext, classify
from fastapi.testclient import TestClient


client = TestClient(app)


def test_load_model():
    load_model() 


def test_classify_endpoint():
    text_data = {"text": "zucker"}
    response = client.post("/classify/", json=text_data)
    assert response.status_code == 200
    assert isinstance(json.loads(response.text), dict)


def test_low_confidence():
    text_data = {"text": "helloworld"}
    response = client.post("/classify/", json=text_data)
    assert response.status_code == 200
    assert json.loads(response.text)['label'] == 'undefined'


def test_invalid_data_type():
    text_data = {"text": 5}
    response = client.post("/classify/", json=text_data)
    result = json.loads(response.text)
    assert response.status_code == 422
    assert result['detail'][0]['type']=='string_type'
    assert result['detail'][0]['msg']=='Input should be a valid string'


def test_long_input():
    text_data = {"text": 'x'*2048}
    response = client.post("/classify/", json=text_data)
    result = json.loads(response.text)
    assert response.status_code == 422
    assert result['detail'][0]['type']=='string_too_long'
    assert result['detail'][0]['msg']=='String should have at most 1024 characters'


def test_short_input():
    text_data = {"text": 'x'}
    response = client.post("/classify/", json=text_data)
    result = json.loads(response.text)
    assert response.status_code == 422
    assert result['detail'][0]['type']=='string_too_short'
    assert result['detail'][0]['msg']=='String should have at least 2 characters'

