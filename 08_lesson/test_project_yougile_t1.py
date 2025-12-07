import requests

key = "Np3AlpINrXuILmBtixfITsT1rxRAijuaNkhJFKvZFTktzZ0Ac+nEDut19cJZN+8i"  # ЗАМЕНИТЬ на свой актуальный токен!
base_url = "https://ru.yougile.com/api-v2"
headers = {"Authorization": f"Bearer {key}"}


def test_create_project():
    body = {
        "title": "Новый проект"
    }
    r = requests.post(f"{base_url}/projects", headers=headers, json=body)
    assert r.status_code == 201


def test_create_project_negative():
    body = {
        "title": "Новый проект"
    }
    # Без headers — негативный тест (неавторизованный)
    r = requests.post(f"{base_url}/projects", json=body)
    assert r.status_code == 401


def test_edit_project():
    body = {
        "title": "Новый проект"
    }
    body2 = {
        "title": "Новый проект 2"
    }
    r = requests.post(f"{base_url}/projects", headers=headers, json=body)
    assert r.status_code == 201
    id = r.json()["id"]
    r2 = requests.put(f"{base_url}/projects/{id}", headers=headers, json=body2)
    assert r2.status_code == 200


def test_edit_project_negative():
    body = {
        "title": "Новый проект"
    }
    body2 = {
        "title": ""
    }
    r = requests.post(f"{base_url}/projects", headers=headers, json=body)
    assert r.status_code == 201
    id = r.json()["id"]
    r2 = requests.put(f"{base_url}/projects/{id}", headers=headers, json=body2)
    assert r2.status_code == 400


def test_get_project():
    body = {
        "title": "Новый проект"
    }
    r = requests.post(f"{base_url}/projects", headers=headers, json=body)
    assert r.status_code == 201
    id = r.json()["id"]
    r2 = requests.get(f"{base_url}/projects/{id}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["title"] == "Новый проект"


def test_get_project_negative():
    id = "hf3ferg4g4h56hn678i"
    r2 = requests.get(f"{base_url}/projects/{id}", headers=headers)
    assert r2.status_code == 404