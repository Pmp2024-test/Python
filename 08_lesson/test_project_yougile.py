import pytest
from project_yougile_final import ProjectYouGile


class TestYouGileProjects:
    """Тесты для методов работы с проектами YouGile"""

    @pytest.fixture
    def api(self):
        return ProjectYouGile()

    @pytest.fixture
    def auth_data(self):
        return {
            'login': 'REPLACE_WITH_LOGIN',
            'password': 'REPLACE_WITH_PASSWORD',
            'companyID': 'REPLACE_WITH_COMPANY_ID',
            'userID': 'REPLACE_WITH_USER_ID'
        }

    @pytest.fixture
    def test_project_data(self, auth_data):
        return {
            'title': 'Тестовый проект',
            'users': {auth_data['userID']: 'admin'}
        }

    # Позитивные тесты

    def test_create_project_positive(self, api, auth_data, test_project_data):
        """Позитивный тест создания проекта"""
        result = api.create_project(
            title=test_project_data['title'],
            users=test_project_data['users'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        assert 'id' in result
        assert result['title'] == test_project_data['title']
        assert result['users'] == test_project_data['users']

    def test_get_project_positive(self, api, auth_data, test_project_data):
        """Позитивный тест получения проекта"""
        # Создаем проект сначала
        project = api.create_project(
            title=test_project_data['title'],
            users=test_project_data['users'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        # Получаем проект
        result = api.get_project_with_id(
            project_id=project['id'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        assert 'id' in result
        assert result['id'] == project['id']
        assert result['title'] == project['title']

    def test_edit_project_positive(self, api, auth_data, test_project_data):
        """Позитивный тест редактирования проекта"""
        # Создаем проект
        project = api.create_project(
            title=test_project_data['title'],
            users=test_project_data['users'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        # Редактируем проект
        new_title = "Обновленное название"
        new_users = {auth_data['userID']: 'manager'}

        result = api.edit_project(
            project_id=project['id'],
            new_title=new_title,
            new_users=new_users,
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        assert result['title'] == new_title
        assert result['users'] == new_users

    # Негатывные тесты

    def test_create_project_negative_empty_title(self, api, auth_data, test_project_data):
        """Негативный тест: создание с пустым названием"""
        with pytest.raises(Exception) as exc_info:
            api.create_project(
                title="",
                users=test_project_data['users'],
                login=auth_data['login'],
                password=auth_data['password'],
                companyID=auth_data['companyID']
            )

        assert "обязательно" in str(exc_info.value)

    def test_create_project_negative_empty_users(self, api, auth_data):
        """Негативный тест: создание без пользователей"""
        with pytest.raises(Exception) as exc_info:
            api.create_project(
                title="Проект без пользователей",
                users={},
                login=auth_data['login'],
                password=auth_data['password'],
                companyID=auth_data['companyID']
            )

        assert "обязателен" in str(exc_info.value)

    def test_get_project_negative_nonexistent(self, api, auth_data):
        """Негативный тест: получение несуществующего проекта"""
        result = api.get_project_with_id(
            project_id="nonexistent-id-123",
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        assert 'error' in result
        assert result['statusCode'] == 404

    def test_edit_project_negative_nonexistent(self, api, auth_data, test_project_data):
        """Негативный тест: редактирование несуществующего проекта"""
        result = api.edit_project(
            project_id="nonexistent-id-456",
            new_title="Новое название",
            new_users=test_project_data['users'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        assert 'error' in result
        assert result['statusCode'] == 404

    def test_edit_project_negative_empty_title(self, api, auth_data, test_project_data):
        """Негативный тест: редактирование с пустым названием"""
        # Создаем проект
        project = api.create_project(
            title=test_project_data['title'],
            users=test_project_data['users'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        # Пытаемся редактировать с пустым названием
        result = api.edit_project(
            project_id=project['id'],
            new_title="",
            new_users=test_project_data['users'],
            login=auth_data['login'],
            password=auth_data['password'],
            companyID=auth_data['companyID']
        )

        assert 'error' in result
        assert result['statusCode'] == 400
