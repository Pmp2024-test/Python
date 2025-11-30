import requests
from datetime import datetime
import uuid


class ProjectYouGile:
    """
    Page Object для работы с YouGile API
    Mock-версия для тестирования
    """

    def __init__(self, base_url="https://ru.yougile.com/api-v2/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.projects = {}  # Mock хранилище проектов

    def get_token(self, login, password, companyID):
        """
        Mock метод получения токена
        """
        # В mock-режиме всегда возвращаем валидный токен
        return f"mock_token_{uuid.uuid4().hex[:16]}"

    def create_project(self, title, users, login, password, companyID):
        """
        Создать проект - [POST] /api-v2/projects
        """
        # Валидация обязательных полей
        if not title:
            raise Exception("Название проекта обязательно")
        if not users:
            raise Exception("Список пользователей обязателен")

        # Создаем проект
        project_id = f"project_{uuid.uuid4().hex[:8]}"
        project_data = {
            "id": project_id,
            "title": title,
            "users": users,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }

        self.projects[project_id] = project_data
        return project_data

    def get_project_with_id(self, project_id, login, password, companyID):
        """
        Получить проект по ID - [GET] /api-v2/projects/{id}
        """
        if project_id in self.projects:
            return self.projects[project_id]
        else:
            return {
                "error": "Project not found",
                "statusCode": 404
            }

    def edit_project(self, project_id, new_title, new_users, login, password, companyID):
        """
        Редактировать проект - [PUT] /api-v2/projects/{id}
        """
        if project_id not in self.projects:
            return {
                "error": "Project not found",
                "statusCode": 404
            }

        # Валидация
        if not new_title:
            return {
                "error": "Title is required",
                "statusCode": 400
            }
        if not new_users:
            return {
                "error": "Users are required",
                "statusCode": 400
            }

        # Обновляем проект
        self.projects[project_id].update({
            "title": new_title,
            "users": new_users,
            "updatedAt": datetime.now().isoformat()
        })

        return self.projects[project_id]
