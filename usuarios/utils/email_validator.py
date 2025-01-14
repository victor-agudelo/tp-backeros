import re

email_regex = (
    r'^(?!\.)'
    r'(?!.*\.\.)'
    r'[A-Za-z0-9._%+-]+'
    r'@[A-Za-z0-9]+'
    r'(\.[A-Za-z0-9-]+)*'
    r'\.[A-Za-z]{2,63}$'
)

def check_email(email: str) -> bool:
    return True if re.fullmatch(email_regex, email) else False
