import requests



base_url='http://localhost:8080'

def test_get_apps_empty():
    jsonf = {
        'id': 100,
    }
    requests.post(f'{base_url}/queue/', json=jsonf).json()
    resp=requests.get(f'{base_url}/queue/100').json()
    assert resp==[]

def test_new_application_success():
    jsonf={
        'id': 101,
    }
    resp = requests.post(f'{base_url}/queue/', json=jsonf).json()
    assert resp['id']==101
