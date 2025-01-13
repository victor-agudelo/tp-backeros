import string
import random
import secrets


class PasswordGenerator:
    def __init__(self, password_longitude=12):
        self.password_longitude = password_longitude
        self.possible_characters = string.ascii_letters + \
            string.digits + string.punctuation
        self.password = ""

    def create_new_password(self):
        password = []

        password.append(random.choice(string.ascii_lowercase))
        password.append(random.choice(string.ascii_uppercase))
        password.append(random.choice(string.digits))
        password.append(random.choice(string.punctuation))

        while len(password) < self.password_longitude:
            password.append(secrets.choice(self.possible_characters))

        random.shuffle(password)

        self.password = "".join(password)

        return self.password


password_generator = PasswordGenerator()
