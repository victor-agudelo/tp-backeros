import pytest
from datetime import datetime, date
from utils.age_calculator import validate_age


def test_validate_age_with_date_object():
    age = date(2000, 1, 1)
    result = validate_age(age)
    expected = (date.today() - age).days // 365.25
    assert result == expected

def test_validate_age_with_string():
    age = "2000-01-01"
    result = validate_age(age)
    expected = (date.today() - datetime.strptime(age, '%Y-%m-%d').date()).days // 365.25
    assert result == expected

def test_validate_age_with_invalid_string():
    age = "invalid-date"
    with pytest.raises(ValueError):
        validate_age(age)

def test_validate_age_with_invalid_type():
    age = 25.5
    with pytest.raises(TypeError):
        validate_age(age)

def test_validate_age_with_future_date():
    future_date = date.today().replace(year=date.today().year + 1)
    result = validate_age(future_date)
    assert result < 0
