import pytest
from sqlalchemy import text


# Тест 1: Добавление студента
def test_add_student(db):
    """Тест добавления нового студента"""
    import random
    user_id = random.randint(10000, 99999)

    db.execute(
        text(
            "INSERT INTO student (user_id, level, education_form, subject_id) "
            "VALUES (:user_id, :level, :education_form, :subject_id)"
        ),
        {
            "user_id": user_id,
            "level": "Beginner",
            "education_form": "group",
            "subject_id": 1
        }
    )

    # Проверяем, что студент добавлен
    result = db.execute(
        text("SELECT * FROM student WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    # Проверки
    assert result is not None
    assert result[0] == user_id
    assert result[1] == "Beginner"

    print(f"Добавлен студент с ID: {user_id}")


# Тест 2: Изменение студента
def test_update_student(db):
    """Тест изменения данных студента"""
    # Сначала добавляем студента
    import random
    user_id = random.randint(10000, 99999)

    db.execute(
        text(
            "INSERT INTO student (user_id, level, education_form, subject_id) "
            "VALUES (:id, :level, :form, :subject)"
        ),
        {
            "id": user_id,
            "level": "Beginner",
            "form": "group",
            "subject": 1
        }
    )

    # Меняем уровень
    db.execute(
        text("UPDATE student SET level = :new_level WHERE user_id = :id"),
        {"new_level": "Advanced", "id": user_id}
    )

    # Проверяем изменение
    result = db.execute(
        text("SELECT level FROM student WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    assert result[0] == "Advanced"
    print(f"Обновлен студент с ID: {user_id}")


# Тест 3: Удаление студента
def test_delete_student(db):
    """Тест удаления студента"""
    # Сначала добавляем студента
    import random
    user_id = random.randint(10000, 99999)

    db.execute(
        text(
            "INSERT INTO student (user_id, level, education_form, subject_id) "
            "VALUES (:id, :level, :form, :subject)"
        ),
        {
            "id": user_id,
            "level": "Intermediate",
            "form": "personal",
            "subject": 2
        }
    )

    # Удаляем студента
    db.execute(
        text("DELETE FROM student WHERE user_id = :id"),
        {"id": user_id}
    )

    # Проверяем, что студента нет
    result = db.execute(
        text("SELECT COUNT(*) FROM student WHERE user_id = :id"),
        {"id": user_id}
    ).fetchone()

    assert result[0] == 0
    print(f"Удален студент с ID: {user_id}")
