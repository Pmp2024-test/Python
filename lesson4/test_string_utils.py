import pytest
from string_utils import StringUtils


string_utils = StringUtils()


# Тесты для метода capitalize

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),
    ])
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.parametrize("input_str, expected_output", [
    ("09 марта 1983", "09 марта 1983"),
])
def test_capitalize(input_str, expected_output):
    utils = StringUtils()
    result = utils.capitalize(input_str)
    assert result == expected_output


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected_output", [
    (" ", " ")
])
def test_capitalize_negative(input_str, expected_output):
    assert string_utils.capitalize(" ") == " "


# Пример для функции trim

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected_output", [
    ("   Skypro", "Skypro"),
])
def test_trim_positive(input_str, expected_output):
    string_utils = StringUtils()
    result = string_utils.trim(input_str)
    assert result == expected_output


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected_output", [
    ("", ""),
])
def test_trim_negative(input_str, expected_output):
    assert string_utils.trim("") == ""


# Тесты для метода contains

@pytest.mark.positive
def test_contains_positive():
    assert string_utils.contains("SkyPro", "S") is True


@pytest.mark.negative
def test_contains_negative():
    assert string_utils.contains("SkyPro", "U") is False


# Тесты для метода delete_symbol

@pytest.mark.positive
def test_delete_symbol_positive():
    assert string_utils.delete_symbol("SkyPro", "k") == "SyPro"


@pytest.mark.negative
def test_delete_symbol_negative_1():
    assert string_utils.delete_symbol("SkyPro", "z") == "SkyPro"


def test_delete_symbol_negative_2():
    assert string_utils.delete_symbol("", "k") == ""
