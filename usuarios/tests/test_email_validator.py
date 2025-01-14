import pytest
from utils.email_validator import check_email  # Cambia 'your_module' por el nombre del archivo donde está la función


def test_check_email_valid():
    valid_emails = [
        "test@example.com",
        "user.name+tag+sorting@example.com",
        "user_name@sub.example.co.uk",
        "user-name123@example.org",
        "1234567890@example.com",
        "email@domain.com",
    ]
    for email in valid_emails:
        assert check_email(email), f"Expected True for valid email: {email}"

def test_check_email_invalid():
    invalid_emails = [
        "plainaddress",
        "@missingusername.com",
        "username@.com.my",
        "username@domain,com",
        "username@domain..com",
        "user name@domain.com",
        "user@domain@domain.com",
        ".user@domain.com",
        "user@.domain.com",
    ]
    for email in invalid_emails:
        assert not check_email(email), f"Expected False for invalid email: {email}"

def test_check_email_empty_string():
    assert not check_email(""), "Expected False for empty string"

def test_check_email_none():
    with pytest.raises(TypeError):
        check_email(None)

def test_check_email_edge_cases():
    edge_cases = {
        "user@domain.c": False,
        "user@domain.com1": False,
        "user@domain.toolongtldersdfsfdsdfsdfsdfdsfsfwefwrewrwrwrwrwrwrewrwefwerwerwre": False,
        "u@domain.com": True,
        "user@do.co": True,
    }
    for email, expected in edge_cases.items():
        assert check_email(email) == expected, f"Unexpected result for email: {email}"
