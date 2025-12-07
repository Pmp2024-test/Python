import pytest
from sqlalchemy import create_engine, text

# Строка подключения к вашей БД
DATABASE_URL = "postgresql://postgres:123@localhost:5432/QA"

@pytest.fixture
def db():
    """Простая фикстура для работы с БД"""
    # Создаем подключение
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    
    # Начинаем транзакцию
    connection.execute(text("BEGIN"))
    
    yield connection
    
    # Откатываем транзакцию после теста
    connection.execute(text("ROLLBACK"))
    connection.close()
    engine.dispose()
