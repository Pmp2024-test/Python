import pytest
from string_utils import StringUtils

string_utils = StringUtils()


@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected_output", [
    ("Skypro", "Skypro"),
])

def test_capitalize(input_str, expected_output):
    utils = StringUtils()
    result = utils.capitalize(input_str)
    assert result == expected_output


@pytest.mark.parametrize("input_str", [
    ("09 марта 1983"),
])

def test_capitalize(expected_output):
    utils = StringUtils()
    result = utils.capitalize(input_str)
    assert result == expected_output


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected_output", [
    (" ", " ")
])

def test_capitalize(input_str, expected_output):
    utils = StringUtils()
    result = utils.capitalize(input_str)
    assert result == expected_output


@pytest.mark.parametrize("input_str", [
    (""),
])

def test_capitalize(input_str):
    utils = StringUtils()
    result = utils.capitalize(input_str)
    assert result == input_str
