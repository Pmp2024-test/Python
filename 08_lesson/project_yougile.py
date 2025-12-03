import requests


class ProjectYouGile:
    # Инициализация
    def __init__(self, url) -> None:
        self.url = url

    # Получить список проектов компании
    def get_project_list(self, login, password, name):
        payload = {
            'login': login,
            'password': password,
            'name': name
        }
        resp = requests.post(self.url + 'auth/companies', json=payload)
        return resp.json()

    # Получить ключ авторизации
    def get_token(self, login, password, companyID):
        payload = {
            "login": login,
            "password": password,
            "companyID": companyID
        }
        resp = requests.post(self.url + 'auth/keys', json=payload)
        response_data = resp.json()
    
        # Извлекаем токен из ответа
        if 'key' in response_data:
            return response_data['key']
        else:
            raise ValueError("Токен не найден в ответе API")

    # Добавить компанию:
    def create_project(self, title, users, login, password, companyID):
        key = self.get_token(login=login,
                             password=password, companyID=companyID)
        headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json; charset=utf-8'
        }
        project = {
            "title": title,
            "users": users
        }
        resp = requests.post(self.url + 'projects',
                             headers=headers,
                             json=project)
        return resp.json()

        # Получить проект по id
    def get_project_with_id(self, project_id, login, password, companyID):
        key = self.get_token(login=login, password=password, companyID=companyID)
        headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json; charset=utf-8'
        }
        resp = requests.get(self.url + f'projects/{project_id}',
                            headers=headers)
        return resp.json()

    # Изменить название проекта
    def edit_project(self, project_id, new_deleted, new_title, new_users):
        key = self.get_token()
        headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json; charset=utf-8'
        }
        project = {
            "deleted": new_deleted,
            "title": new_title,
            "users": new_users
        }
        resp = requests.put(self.url + f'projects/{project_id}',
                            headers=headers, json=project)
        return resp.json()
